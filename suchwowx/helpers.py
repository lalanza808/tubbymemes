import ipfsApi
from eth_account.messages import encode_defunct

from suchwowx.models import Meme
from suchwowx.factory import w3
from suchwowx import config


def get_eth_contract():
    """
    Return a web3 contract object with the currently
    deployed SuchWowX smart contract.
    """
    contract_abi = config.CONTRACT_ABI
    contract_address = w3.toChecksumAddress(config.CONTRACT_ADDRESS)
    return w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )


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
        client = ipfsApi.Client('127.0.0.1', 5001)
        artwork_hashes = client.add(meme.get_fs_path())
        artwork_hash = artwork_hashes[0]['Hash']
        print(f'[+] Uploaded artwork to IPFS: {artwork_hash}')
        meta = {
            'name': meme.title,
            'description': meme.description,
            'image': f'ipfs://{artwork_hash}',
            'create_date': meme.create_date.strftime('%Y-%m-%d %H:%M:%S'),
            'file_name': meme.file_name,
            'ipfs_hash': artwork_hash,
            'properties': {
                'creator_handle': meme.user.handle,
                'creator_address': meme.user.public_address
            }
        }
        meta_hash = client.add_json(meta)
        print(f'[+] Uploaded metadata to IPFS: {meta_hash}')
        return (meta_hash, artwork_hash)
    except Exception as e:
        print(f'[!] Error: {e}')
        return False
