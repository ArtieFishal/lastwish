from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.wallet import WalletSession

wallet_bp = Blueprint('wallet_bp', __name__)

@wallet_bp.route('/', methods=['POST'])
@jwt_required()
def add_wallet():
    """
    Adds a new wallet and its assets to the user's estate plan.
    This is called from the frontend after fetching assets.
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        if not data or not 'address' in data or not 'network' in data:
            return jsonify({'error': 'Missing required wallet data'}), 400

        existing_wallet = WalletSession.find_by_wallet(user_id, data['address'])
        if existing_wallet:
            if 'assets' in data:
                existing_wallet.update_assets(data['assets'])
            if 'beneficiary' in data:
                 existing_wallet.assign_beneficiary('all_assets', data['beneficiary'])
            existing_wallet.save()
            return jsonify(existing_wallet.to_dict()), 200

        new_wallet = WalletSession.create(
            user_id=user_id,
            wallet_address=data['address'],
            blockchain=data['network'],
            wallet_type=data.get('type', 'unknown')
        )

        if 'assets' in data and data['assets']:
            new_wallet.update_assets(data['assets'])

        if 'beneficiary' in data and data['beneficiary']:
            new_wallet.assign_beneficiary(
                asset_symbol='all_assets',
                beneficiary_data=data['beneficiary']
            )

        return jsonify(new_wallet.to_dict()), 201

    except Exception as e:
        # In a real app, you'd want more sophisticated logging
        print(f"An exception occurred in add_wallet: {e}")
        return jsonify({'error': 'An internal error occurred'}), 500

@wallet_bp.route('/', methods=['GET'])
@jwt_required()
def get_wallets():
    """
    Gets all wallets for the current user.
    """
    try:
        user_id = get_jwt_identity()
        wallets = WalletSession.find_by_user(user_id)
        return jsonify([w.to_dict() for w in wallets]), 200
    except Exception as e:
        print(f"An exception occurred in get_wallets: {e}")
        return jsonify({'error': 'An internal error occurred'}), 500
