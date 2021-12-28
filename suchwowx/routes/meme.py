from os import path
from secrets import token_urlsafe
from json import loads, dumps

import ipfsApi
from flask import Blueprint, render_template, request, current_app
from flask import send_from_directory, redirect, flash, url_for, jsonify
from flask_login import logout_user, current_user, login_user
from requests.exceptions import HTTPError
from web3 import Web3

from suchwowx.models import Meme, User
from suchwowx.factory import db
from suchwowx import config


bp = Blueprint('meme', 'meme')

@bp.route('/')
def index():
    memes = Meme.query.filter(Meme.meta_ipfs_hash != None).order_by(Meme.create_date.desc())
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:9650'))
    contract_address = w3.toChecksumAddress(config.CONTRACT_ADDRESS)
    contract_abi = config.CONTRACT_ABI
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )
    # total_supply = contract.functions.totalSupply().call()
    return render_template('index.html', memes=memes, contract=contract)

@bp.route('/mod')
def mod():
    if not current_user.is_moderator():
        flash('You are not a moderator', 'warning')
        return redirect(url_for('meme.index'))
    memes = Meme.query.filter(
        Meme.meta_ipfs_hash == None
    ).order_by(Meme.create_date.desc())
    return render_template('review.html', memes=memes)

@bp.route('/publish', methods=['GET', 'POST'])
def publish():
    if not current_user.is_authenticated:
        flash('You need to connect your wallet first.', 'warning')
        return redirect(url_for('meme.index'))
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
        return redirect(url_for('meme.index'))
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
            meta_hash = None
            artwork_hash = None
            if current_user.verified or current_user.is_moderator():
                client = ipfsApi.Client('127.0.0.1', 5001)
                artwork_hashes = client.add(full_path)
                print(artwork_hashes)
                artwork_hash = artwork_hashes[0]['Hash']
                print(artwork_hash)
                print(f'[+] Uploaded artwork to IPFS: {artwork_hash}')
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
                print(f'[+] Uploaded metadata to IPFS: {meta_hash}')
                flash('Published new meme to IPFS', 'success')
            meme = Meme(
                file_name=filename,
                meta_ipfs_hash=meta_hash,
                meme_ipfs_hash=artwork_hash,
                title=title,
                description=description,
                creator_handle=creator
            )
            db.session.add(meme)
            db.session.commit()
            flash('Published new meme to database', 'success')
            return redirect(url_for('meme.index'))
        except ConnectionError:
            flash('[!] Unable to connect to local ipfs', 'error')
        except Exception as e:
            print(e)
    return render_template(
        'publish.html',
        meme=meme
    )


@bp.route('/meme/<meme_id>')
def meme(meme_id):
    meme = Meme.query.filter(Meme.id == meme_id).first()
    if not meme:
        return redirect('/')
    if not meme.meta_ipfs_hash and not current_user.is_authenticated:
        flash('You need to be a moderator to view that meme', 'warning')
        return redirect(url_for('meme.index'))
    elif not meme.meta_ipfs_hash and not current_user.is_moderator():
        flash('You need to be a moderator to view that meme', 'warning')
        return redirect(url_for('meme.index'))
    return render_template('meme.html', meme=meme)
