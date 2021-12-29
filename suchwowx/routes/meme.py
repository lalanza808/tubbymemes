from os import path, remove
from secrets import token_urlsafe
from json import loads, dumps

import ipfsApi
from flask import Blueprint, render_template, request, current_app
from flask import send_from_directory, redirect, flash, url_for, jsonify
from flask_login import logout_user, current_user, login_user
from requests.exceptions import HTTPError
from web3 import Web3

from suchwowx.models import Meme, User
from suchwowx.helpers import upload_to_ipfs
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
    ).order_by(Meme.create_date.asc())
    return render_template('mod.html', memes=memes)

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
        return redirect(url_for('meme.index') + '?ipfs_error=1')
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
            meme = Meme(
                file_name=filename,
                title=title,
                description=description,
                creator_handle=creator
            )
            db.session.add(meme)
            db.session.commit()
            if current_user.verified or current_user.is_moderator():
                res = upload_to_ipfs(meme.id)
                meme.meta_ipfs_hash = res[0]
                meme.meme_ipfs_hash = res[1]
                db.session.commit()
                flash('Published new meme to local database and IPFS.', 'success')
            else:
                flash('Published new meme to database for review by moderators.', 'success')
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
def show(meme_id):
    meme = Meme.query.filter(Meme.id == meme_id).first()
    if not meme:
        return redirect('/')
    if not meme.meta_ipfs_hash and not current_user.is_authenticated:
        flash('You need to be a moderator to view that meme.', 'warning')
        return redirect(url_for('meme.index'))
    elif not meme.meta_ipfs_hash and not current_user.is_moderator():
        flash('You need to be a moderator to view that meme.', 'warning')
        return redirect(url_for('meme.index'))
    return render_template('meme.html', meme=meme)

@bp.route('/meme/<meme_id>/<action>')
def approve(meme_id, action):
    if not current_user.is_authenticated:
        flash('You need to be logged in to reach this page.', 'warning')
        return redirect(url_for('meme.index'))
    if not current_user.is_moderator():
        flash('You need to be a moderator to reach this page.', 'warning')
        return redirect(url_for('meme.index'))
    meme = Meme.query.get(meme_id)
    if not meme:
        flash('That meme does not exist.', 'warning')
        return redirect(url_for('meme.index'))
    if meme.meta_ipfs_hash != None:
        flash('That meme already has been published to IPFS.', 'warning')
        return redirect(url_for('meme.show', meme_id=meme.id))
    if action == 'approve':
        res = upload_to_ipfs(meme.id)
        if not res:
            flash('Unable to post to IPFS, daemon may be offline.', 'error')
            return redirect(url_for('meme.show', meme_id=meme.id))
        existing_meta_ipfs = Meme.query.filter(Meme.meta_ipfs_hash == res[0]).first()
        existing_meme_ipfs = Meme.query.filter(Meme.meme_ipfs_hash == res[1]).first()
        if existing_meta_ipfs or existing_meme_ipfs:
            flash('Cannot use an existing IPFS hash for either metadata or memes.', 'warning')
            return redirect(url_for('meme.show', meme_id=meme.id))
        meme.meta_ipfs_hash = res[0]
        meme.meme_ipfs_hash = res[1]
        db.session.commit()
        flash('Published new meme to IPFS.', 'success')
    elif action == 'deny':
        # delete image
        # delete from database
        if path.exists(meme.get_fs_path()):
            remove(meme.get_fs_path())
        db.session.delete(meme)
        db.session.commit()
        flash('Deleted image and removed meme from database.', 'success')
    else:
        flash('Unknown action.', 'warning')
    return redirect(url_for('meme.mod'))
