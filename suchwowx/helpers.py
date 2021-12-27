from eth_account.messages import encode_defunct

from suchwowx.factory import w3


def verify_signature(message, signature, public_address):
    msg = encode_defunct(text=message)
    recovered = w3.eth.account.recover_message(msg, signature=signature)
    print(f'found recovered: {recovered}')
    if recovered.lower() == public_address.lower():
        return True
    else:
        return False
