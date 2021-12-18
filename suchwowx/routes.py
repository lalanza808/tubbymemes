import ipfsApi
from os import path
from secrets import token_urlsafe
from json import loads, dumps

from flask import Blueprint, render_template, request, current_app


bp = Blueprint('meta', 'meta')

@bp.route('/', methods=['GET', 'POST'])
def index():
    if "file" in request.files:
        title = request.form.get('title')
        description = request.form.get('description')
        creator = request.form.get('creator')
        file = request.files["file"]
        filename = "{}{}".format(
            token_urlsafe(24),
            path.splitext(file.filename)[1]
        )
        file.save(filename)
        try:
            client = ipfsApi.Client('127.0.0.1', 5001)
            artwork_hash = client.add(filename)['Hash']
            client.pin_add(artwork_hash)
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
            print(meta)
            meta_hash = client.add_json(meta)
            client.pin_add(meta_hash)
            print(f'[+] Uploaded metadata to IPFS: {meta_hash}')
        except ConnectionError:
            print('[!] Unable to connect to local ipfs')
        except Exception as e:
            print(e)
    return render_template('index.html')

@bp.route('/next')
def next():
    return render_template('next.html')
