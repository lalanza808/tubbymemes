import ipfsApi
from eth_account.messages import encode_defunct

from suchwowx.models import Meme
from suchwowx.factory import w3
from suchwowx import config


def verify_signature(message, signature, public_address):
    msg = encode_defunct(text=message)
    recovered = w3.eth.account.recover_message(msg, signature=signature)
    if recovered.lower() == public_address.lower():
        return True
    else:
        return False


def upload_to_ipfs(meme_id: str):
    meme = Meme.query.get(meme_id)
    if not meme:
        return False
    try:
        full_path = f'{config.DATA_FOLDER}/uploads/{meme.file_name}'
        client = ipfsApi.Client('127.0.0.1', 5001)
        artwork_hashes = client.add(full_path)
        artwork_hash = artwork_hashes[0]['Hash']
        print(f'[+] Uploaded artwork to IPFS: {artwork_hash}')
        meta = {
            'name': meme.title,
            'description': meme.description,
            'image': f'ipfs://{artwork_hash}',
            'by': meme.user.handle,
            'properties': {
                'creator': meme.user.handle
            }
        }
        meta_hash = client.add_json(meta)
        print(f'[+] Uploaded metadata to IPFS: {meta_hash}')
        return (meta_hash, artwork_hash)
    except Exception as e:
        print(f'[!] Error: {e}')
        return False
