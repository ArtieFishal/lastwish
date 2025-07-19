"""
Estate Planning API Routes for LastWish Web3
Handles will creation, asset management, beneficiaries, and crypto assets
"""
from flask import Blueprint, request, jsonify, session
from models.user import db, User
from models.estate_models import *
from datetime import datetime
import json

# Create blueprint
estate_bp = Blueprint('estate', __name__)

@estate_bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    """Get estate planning dashboard summary"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Not authenticated'}), 401
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get counts and summaries
        wills_count = Will.query.filter_by(user_id=user_id).count()
        assets_count = Asset.query.filter_by(user_id=user_id).count()
        crypto_assets_count = CryptoAsset.query.filter_by(user_id=user_id).count()
        beneficiaries_count = Beneficiary.query.filter_by(user_id=user_id).count()
        
        # Calculate total asset value
        assets = Asset.query.filter_by(user_id=user_id).all()
        total_asset_value = sum(float(asset.estimated_value or 0) for asset in assets)
        
        # Calculate crypto portfolio value
        crypto_assets = CryptoAsset.query.filter_by(user_id=user_id).all()
        total_crypto_value = sum(float(crypto.estimated_value or 0) for crypto in crypto_assets)
        
        return jsonify({
            'success': True,
            'dashboard': {
                'user': user.to_dict(),
                'summary': {
                    'wills_count': wills_count,
                    'assets_count': assets_count,
                    'crypto_assets_count': crypto_assets_count,
                    'beneficiaries_count': beneficiaries_count,
                    'total_asset_value': total_asset_value,
                    'total_crypto_value': total_crypto_value,
                    'total_portfolio_value': total_asset_value + total_crypto_value
                },
                'recent_activity': [],
                'recommendations': [
                    'Complete your will creation',
                    'Add beneficiaries to your assets',
                    'Set up crypto inheritance'
                ]
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@estate_bp.route('/wills', methods=['GET', 'POST'])
def manage_wills():
    """Get or create wills"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Not authenticated'}), 401
        
        if request.method == 'GET':
            wills = Will.query.filter_by(user_id=user_id).all()
            return jsonify({
                'success': True,
                'wills': [will.to_dict() for will in wills]
            })
        
        elif request.method == 'POST':
            data = request.get_json()
            
            will = Will(
                user_id=user_id,
                title=data.get('title', 'My Will'),
                content=json.dumps(data.get('content', {})),
                status='draft'
            )
            
            db.session.add(will)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'will': will.to_dict(),
                'message': 'Will created successfully'
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@estate_bp.route('/assets', methods=['GET', 'POST'])
def manage_assets():
    """Get or create assets"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Not authenticated'}), 401
        
        if request.method == 'GET':
            assets = Asset.query.filter_by(user_id=user_id).all()
            return jsonify({
                'success': True,
                'assets': [asset.to_dict() for asset in assets]
            })
        
        elif request.method == 'POST':
            data = request.get_json()
            
            asset = Asset(
                user_id=user_id,
                asset_type=data.get('asset_type'),
                name=data.get('name'),
                description=data.get('description'),
                estimated_value=data.get('estimated_value', 0),
                location=data.get('location'),
                account_number=data.get('account_number'),
                institution=data.get('institution')
            )
            
            db.session.add(asset)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'asset': asset.to_dict(),
                'message': 'Asset created successfully'
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@estate_bp.route('/crypto-assets', methods=['GET', 'POST'])
def manage_crypto_assets():
    """Get or create crypto assets"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Not authenticated'}), 401
        
        if request.method == 'GET':
            crypto_assets = CryptoAsset.query.filter_by(user_id=user_id).all()
            return jsonify({
                'success': True,
                'crypto_assets': [asset.to_dict() for asset in crypto_assets]
            })
        
        elif request.method == 'POST':
            data = request.get_json()
            
            crypto_asset = CryptoAsset(
                user_id=user_id,
                asset_type=data.get('asset_type'),
                symbol=data.get('symbol'),
                name=data.get('name'),
                amount=data.get('amount', 0),
                estimated_value=data.get('estimated_value', 0),
                wallet_address=data.get('wallet_address'),
                network=data.get('network'),
                contract_address=data.get('contract_address')
            )
            
            db.session.add(crypto_asset)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'crypto_asset': crypto_asset.to_dict(),
                'message': 'Crypto asset created successfully'
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@estate_bp.route('/beneficiaries', methods=['GET', 'POST'])
def manage_beneficiaries():
    """Get or create beneficiaries"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Not authenticated'}), 401
        
        if request.method == 'GET':
            beneficiaries = Beneficiary.query.filter_by(user_id=user_id).all()
            return jsonify({
                'success': True,
                'beneficiaries': [beneficiary.to_dict() for beneficiary in beneficiaries]
            })
        
        elif request.method == 'POST':
            data = request.get_json()
            
            beneficiary = Beneficiary(
                user_id=user_id,
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                relationship=data.get('relationship'),
                email=data.get('email'),
                phone=data.get('phone'),
                address=data.get('address'),
                date_of_birth=datetime.strptime(data.get('date_of_birth'), '%Y-%m-%d').date() if data.get('date_of_birth') else None,
                wallet_address=data.get('wallet_address'),
                notes=data.get('notes')
            )
            
            db.session.add(beneficiary)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'beneficiary': beneficiary.to_dict(),
                'message': 'Beneficiary created successfully'
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

