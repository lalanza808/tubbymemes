import ipfsApi
from os import path
from secrets import token_urlsafe
from json import loads, dumps

from flask import Blueprint, render_template, request, current_app, redirect

from suchwowx.models import Meme
from suchwowx.factory import db
from suchwowx import config


bp = Blueprint('meta', 'meta')

@bp.route('/new', methods=['GET', 'POST'])
def new():
    meme = None
    if "file" in request.files:
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
            print('[!] Unable to connect to local ipfs')
        except Exception as e:
            print(e)
    return render_template(
        'new.html',
        meme=meme
    )

@bp.route('/')
def index():
    memes = Meme.query.filter().order_by(Meme.create_date.desc())
    return render_template('index.html', memes=memes)
