from os import path
from secrets import token_urlsafe
from json import loads, dumps

import ipfsApi
from flask import Blueprint, render_template, request, current_app
from flask import send_from_directory, redirect, flash, url_for
from requests.exceptions import HTTPError
from web3 import Web3

from suchwowx.models import Meme
from suchwowx.factory import db
from suchwowx import config


bp = Blueprint('meta', 'meta')

@bp.route('/')
def index():
    memes = Meme.query.filter().order_by(Meme.create_date.desc())
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:9650'))
    contract_address = w3.toChecksumAddress(config.CONTRACT_ADDRESS)
    contract_abi = config.CONTRACT_ABI
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )
    # total_supply = contract.functions.totalSupply().call()
    return render_template('index.html', memes=memes, contract=contract)

@bp.route('/new', methods=['GET', 'POST'])
def new():
    meme = None
    form_err = False
    try:
        client = ipfsApi.Client('127.0.0.1', 5001)
        client.add_json({})
    except Exception as e:
        msg = f'[!] IPFS Error: {e}'
        print(msg)
        flash(msg, 'error')
        if "file" in request.files:
            return '<script>window.history.back()</script>'
        return redirect(url_for('meta.index'))
    if "file" in request.files:
        if form_err:
            return '<script>window.history.back()</script>'
        title = request.form.get('title')
        description = request.form.get('description')
        creator = request.form.get('creator')
        file = request.files["file"]
        filename = "{}{}".format(
            token_urlsafe(24),
            path.splitext(file.filename)[1]
        )
        full_path = f'{config.DATA_FOLDER}/uploads/{filename}'
        file.save(full_path)
        try:
            client = ipfsApi.Client('127.0.0.1', 5001)
            artwork_hashes = client.add(full_path)
            print(artwork_hashes)
            artwork_hash = artwork_hashes[0]['Hash']
            print(artwork_hash)
            # client.pin_add(artwork_hash)
            print(f'[+] Uploaded artwork to IPFS: {artwork_hash}')
            # Create meta json
            meta = {
                'name': title,
                'description': description,
                'image': f'ipfs://{artwork_hash}',
                'by': creator,
                'properties': {
                    'creator': creator
                }
            }
            meta_hash = client.add_json(meta)
            # client.pin_add(meta_hash)
            print(f'[+] Uploaded metadata to IPFS: {meta_hash}')
            meme = Meme(
                upload_path=filename,
                meta_ipfs_hash=meta_hash,
                meme_ipfs_hash=artwork_hash,
                title=title,
                description=description,
                creator_handle=creator
            )
            db.session.add(meme)
            db.session.commit()
            return redirect('/')
        except ConnectionError:
            flash('[!] Unable to connect to local ipfs', 'error')
        except Exception as e:
            print(e)
    return render_template(
        'new.html',
        meme=meme
    )

@bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """
    Retrieve an uploaded file from uploads directory.
    """
    return send_from_directory(f'{config.DATA_FOLDER}/uploads', filename)

@bp.route('/meme/<meme_id>')
def meme(meme_id):
    meme = Meme.query.filter(Meme.id == meme_id).first()
    if not meme:
        return redirect('/')
    return render_template('meme.html', meme=meme)

@bp.route('/creator/<handle>')
def creator(handle):
    return render_template('includes/creator.html')
