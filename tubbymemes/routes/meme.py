from os import path, remove
from secrets import token_urlsafe

import ipfsApi
from flask import Blueprint, render_template, request
from flask import redirect, flash, url_for
from flask_login import current_user
from web3 import Web3

from tubbymemes.models import Meme
from tubbymemes.helpers import upload_to_ipfs
from tubbymemes.factory import db
from tubbymemes import config


bp = Blueprint('meme', 'meme')


@bp.route('/')
def index():
    memes = Meme.query.filter(
        Meme.approved == True
    ).order_by(Meme.create_date.desc())
    return render_template('index.html', memes=memes)


@bp.route('/mod')
def mod():
    if not current_user.is_authenticated:
        flash('You must be logged in and have MetaMask wallet connected.', 'warning')
        return redirect(url_for('meme.index'))
    if not current_user.is_moderator():
        flash('You are not a moderator.', 'warning')
        return redirect(url_for('meme.index'))
    memes = Meme.query.filter(
        Meme.approved != True
    ).order_by(Meme.create_date.asc())
    return render_template('index.html', memes=memes)


@bp.route('/publish', methods=['GET', 'POST'])
def publish():
    if not current_user.is_authenticated:
        flash('You need to connect your wallet first.', 'warning')
        return redirect(url_for('meme.index'))
    if not current_user.wownero_address:
        flash('You need to specify your Wownero wallet address first.', 'warning')
        return redirect(url_for('user.show', handle=current_user.handle))
    meme = None
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
        title = request.form.get('title')
        description = request.form.get('description')
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
                user_id=current_user.id
            )
            db.session.add(meme)
            db.session.commit()
            if current_user.verified or current_user.is_moderator():
                res = upload_to_ipfs(meme.id)
                meme.meta_ipfs_hash = res[0]
                meme.meme_ipfs_hash = res[1]
                meme.approved = True
                db.session.commit()
                flash('Published new meme to local database and IPFS.', 'success') # noqa
            else:
                flash('Published new meme to database for review by moderators.', 'success') # noqa
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
    if not meme.approved and not current_user.is_authenticated:
        flash('You need to be logged in to view that meme.', 'warning')
        return redirect(url_for('meme.index'))
    elif not meme.approved and not current_user.is_moderator():
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
    if meme.approved is True:
        flash('That meme already has been approved.', 'warning')
        return redirect(url_for('meme.show', meme_id=meme.id))
    if action == 'approve':
        res = upload_to_ipfs(meme.id)
        if not res:
            flash('Unable to post to IPFS, daemon may be offline.', 'error')
            return redirect(url_for('meme.show', meme_id=meme.id))
        existing_meta_ipfs = Meme.query.filter(
            Meme.meta_ipfs_hash == res[0]
        ).first()
        existing_meme_ipfs = Meme.query.filter(
            Meme.meme_ipfs_hash == res[1]
        ).first()
        if meme.synced is False:
            if existing_meta_ipfs or existing_meme_ipfs:
                flash('Cannot use an existing IPFS hash for either metadata or memes on new posts.', 'warning') # noqa
                return redirect(url_for('meme.show', meme_id=meme.id))
            meme.meta_ipfs_hash = res[0]
            meme.meme_ipfs_hash = res[1]
        meme.approved = True
        db.session.commit()
        flash('Approved meme and published new meme to local IPFS server.', 'success')
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
