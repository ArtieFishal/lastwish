import traceback
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.wallet import WalletSession, to_json

wallet_bp = Blueprint('wallet_bp', __name__)

@wallet_bp.route('/', methods=['POST'])
@jwt_required()
def add_wallet():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        if not data or 'address' not in data or 'network' not in data:
            return jsonify({'error': 'Missing required wallet data'}), 400

        existing_wallet = WalletSession.find_by_wallet(user_id, data['address'])

        if existing_wallet:
            wallet_id = existing_wallet['_id']
            if 'assets' in data: WalletSession.add_assets(wallet_id, data['assets'])
            if 'beneficiary' in data: WalletSession.add_beneficiary(wallet_id, data['beneficiary'])
            updated_wallet = WalletSession.find_by_wallet(user_id, data['address'])
            return jsonify(to_json(updated_wallet)), 200
        else:
            new_wallet_doc = WalletSession.create(
                user_id=user_id, wallet_address=data['address'],
                blockchain=data['network'], wallet_type=data.get('type', 'unknown')
            )
            wallet_id = new_wallet_doc['_id']
            if 'assets' in data: WalletSession.add_assets(wallet_id, data['assets'])
            if 'beneficiary' in data: WalletSession.add_beneficiary(wallet_id, data['beneficiary'])
            created_wallet = WalletSession.find_by_wallet(user_id, data['address'])
            return jsonify(to_json(created_wallet)), 201

    except Exception:
        traceback.print_exc()
        return jsonify({'error': 'An internal error occurred'}), 500

@wallet_bp.route('/', methods=['GET'])
@jwt_required()
def get_wallets():
    try:
        user_id = get_jwt_identity()
        wallets = WalletSession.find_by_user(user_id)
        return jsonify(to_json(wallets)), 200
    except Exception:
        traceback.print_exc()
        return jsonify({'error': 'An internal error occurred'}), 500
