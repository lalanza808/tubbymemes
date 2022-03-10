import requests
from flask import Blueprint
from secrets import token_urlsafe
from datetime import datetime

from tubbymemes.factory import db
from tubbymemes.helpers import get_eth_contract
from tubbymemes.models import Meme, User, Remote
from tubbymemes import config


bp = Blueprint('cli', 'cli', cli_group=None)


@bp.cli.command('init')
def init():
    db.create_all()

@bp.cli.command('sync-avax')
def sync_avax():
    """
    Synchronize your local database with the tokens minted on Avalanche blockchain.
    """
    contract = get_eth_contract()
    total_supply = contract.functions.totalSupply().call()
    # walk backwards through all tokens at top of supply
    # until you've accounted for the last known
    for i in range(total_supply, 0, -1):
        # first get metadata ipfs hash
        deets = contract.functions.tokenMeme(i).call()
        try:
            meme_exists = Meme.query.filter(Meme.meta_ipfs_hash == deets[8]).first() # noqa
            user_exists = User.query.filter(User.public_address == deets[6].lower()).first() # noqa
            if meme_exists:
                if not meme_exists.minted:
                    meme_exists.minted = True
                    db.session.commit()
                    print(f'[+] Marked existing meme {meme_exists.id} as minted')
            else:
                print(deets)
                if not user_exists:
                    user_exists = User(
                        public_address=deets[4].lower()
                    )
                    db.session.add(user_exists)
                    db.session.commit()
                    user_exists.handle = f'anon{user_exists.id}-{token_urlsafe(6)}'
                    db.session.commit()
                    print(f'[+] Created user {user_exists.handle}')
                res = requests.get(f'{config.IPFS_SERVER}/ipfs/{deets[5]}', timeout=30).json()
                if not 'image' in res:
                    print('No image IPFS hash, skipping')
                    continue
                meme_ipfs_hash = res['image'].split('ipfs://')[1]
                filename = token_urlsafe(24)
                print(f'[+] Downloading image hash {meme_ipfs_hash} as {filename}')
                r = requests.get(f'{config.IPFS_SERVER}/ipfs/{meme_ipfs_hash}', stream=True)
                with open(f'{config.DATA_FOLDER}/uploads/{filename}', 'wb') as f:
                    for chunk in r.iter_content(chunk_size = 16*1024):
                        f.write(chunk)
                meme = Meme(
                    title=res['name'],
                    file_name=filename,
                    description=res['description'],
                    user_id=user_exists.id,
                    meta_ipfs_hash=deets[5],
                    meme_ipfs_hash=meme_ipfs_hash,
                    minted=True,
                    synced=True
                )
                db.session.add(meme)
                db.session.commit()
                print(f'[+] Added new meme {meme.id}')
        except Exception as e:
            print(e)


@bp.cli.command('sync-remotes')
def sync_remotes():
    """
    Sync remote servers with local database.
    """
    from pprint import pprint
    remotes = Remote.query.filter(Remote.paused == False)
    for remote in remotes:
        print(f'[+] Fetching approved memes from remote {remote.id} ({remote.endpoint})')
        deets = requests.get(remote.endpoint + '/api/v1/memes').json()
        for meme_id in deets:
            meme = deets[meme_id]
            user = meme['user']
            meme_exists = Meme.query.filter(Meme.meta_ipfs_hash == meme['meta_ipfs_hash']).first() # noqa
            user_exists = User.query.filter(User.public_address == user['public_address'].lower()).first() # noqa
            if not meme_exists:
                if not user_exists:
                    user_exists = User(
                        public_address=user['public_address'].lower(),
                        bio=user['bio'],
                        ipfs_hash=user['ipfs_hash'],
                        profile_image=user['profile_image'],
                        website_url=user['website_url'],
                        wownero_address=user['wownero_address'],
                        handle=user['handle']
                    )
                    db.session.add(user_exists)
                    db.session.commit()
                    print(f'[+] Created user {user_exists.handle}')
                print(f'[+] Downloading image hash {meme["meme_ipfs_hash"]} as {meme["file_name"]}')
                r = requests.get(f'{config.IPFS_SERVER}/ipfs/{meme["meme_ipfs_hash"]}', stream=True)
                with open(f'{config.DATA_FOLDER}/uploads/{meme["file_name"]}', 'wb') as f:
                    for chunk in r.iter_content(chunk_size = 16*1024):
                        f.write(chunk)
                meme = Meme(
                    title=meme['title'],
                    file_name=meme['file_name'],
                    description=meme['description'],
                    user_id=user_exists.id,
                    meta_ipfs_hash=meme['meta_ipfs_hash'],
                    meme_ipfs_hash=meme['meme_ipfs_hash'],
                    minted=meme['minted'],
                    synced=True
                )
                db.session.add(meme)
                db.session.commit()
                print(f'[+] Added new meme {meme.id}')
            remote.last_sync_date = datetime.utcnow()
            db.session.commit()