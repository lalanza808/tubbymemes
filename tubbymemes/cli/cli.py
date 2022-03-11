import requests
from flask import Blueprint
from secrets import token_urlsafe
from datetime import datetime

from tubbymemes.factory import db
from tubbymemes.models import Meme, User, Remote
from tubbymemes import config


bp = Blueprint('cli', 'cli', cli_group=None)


@bp.cli.command('init')
def init():
    db.create_all()


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
                    )
                    db.session.add(user_exists)
                    db.session.commit()
                    print(f'[+] Created user {user_exists.public_address}')
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
