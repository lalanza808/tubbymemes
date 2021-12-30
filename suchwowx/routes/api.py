from secrets import token_urlsafe

from flask import Blueprint, request, jsonify
from flask_login import current_user

from suchwowx.factory import db
from suchwowx.helpers import verify_signature
from suchwowx.models import User


bp = Blueprint('api', 'api', url_prefix='/api/v1')


@bp.route('/user_exists')
def user_exists():
    """
    Check to see if a given user exists (handle or wallet address).
    This logic will help the login/connect MetaMask flow.
    """
    if 'public_address' in request.args:
        query_str = 'public_address'
        query_field = User.public_address
    elif 'handle' in request.args:
        query_str = 'handle'
        query_field = User.handle
    else:
        return jsonify({'success': False})

    u = User.query.filter(
        query_field == request.args[query_str].lower()
    ).first()
    if u:
        nonce = u.nonce
    else:
        nonce = User().generate_nonce()
    return jsonify({
        'user_exists': u is not None,
        'nonce': nonce,
        'query': query_str,
        'success': True
    })


@bp.route('/update/user', methods=['POST'])
def update_user():
    if not current_user.is_authenticated:
        return jsonify({
            'success': False,
            'message': 'Must be authenticated in order to update.'
        })

    data = request.get_json()
    _u = User.query.get(int(data['user_id']))

    if _u:
        if current_user.id == _u.id:
            user_exists = User.query.filter(
                User.handle == data['handle']
            ).first()
            if user_exists and not current_user.id == user_exists.id:
                return jsonify({
                    'success': False,
                    'message': 'That user handle already exists on this server'
                })
            _u.wownero_address = data['wownero_address']
            _u.ipfs_hash = data['ipfs_hash']
            _u.handle = data['handle']
            db.session.commit()
            return jsonify({
                'success': True,
                'message': 'Updated user record.'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Cannot edit another record.'
            })

    else:
        return jsonify({
            'success': False,
            'message': 'User does not exist.'
        })


@bp.route('/authenticate/metamask', methods=['POST'])
def authenticate_metamask():
    """
    This is the login/authenticate route for this dApp.
    Users POST a `signedData` blob, a message signed by the user with MetaMask
    (`personal_sign` method).

    This route will verify the signed data against the user's public ETH
    address. If no user exists, they get an entry in the database with a
    default handle assigned. If user does exist, they get logged in.
    """
    data = request.get_json()
    if current_user.is_authenticated:
        return jsonify({
            'success': False,
            'message': 'Already registered and authenticated.'
        })

    _u = User.query.filter_by(
        public_address=data['public_address'].lower()
    ).first()

    if _u:
        if data['message'].endswith(_u.nonce):
            if verify_signature(data['message'], data['signed_data'], data['public_address']): # noqa
                _u.login()
                return jsonify({
                    'success': True,
                    'message': 'Logged in'
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Invalid signature'
                })
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid nonce in signed message'
            })
    else:
        rand_str = token_urlsafe(6)
        user = User(
            public_address=data['public_address'].lower()
        )
        db.session.add(user)
        db.session.commit()
        user.handle = f'anon{user.id}-{rand_str}'
        db.session.commit()
        user.login()
        return jsonify({
            'success': True,
            'message': 'Registered'
        })
