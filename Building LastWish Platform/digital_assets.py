from flask import Blueprint, request, jsonify, session
from src.models.user import User, db
from src.models.estate import DigitalAsset, Beneficiary, AuditLog
from datetime import datetime
from decimal import Decimal

digital_assets_bp = Blueprint('digital_assets', __name__)

def require_auth():
    """Check if user is authenticated"""
    user_id = session.get('user_id')
    if not user_id:
        return None
    return User.query.get(user_id)

def log_audit_action(user_id, action, resource_type, resource_id=None, description=None):
    """Log audit action"""
    try:
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            description=description,
            ip_address=request.remote_addr
        )
        db.session.add(audit_log)
        db.session.commit()
    except Exception as e:
        print(f"Failed to log audit action: {e}")

@digital_assets_bp.route('/', methods=['GET'])
def get_digital_assets():
    """Get all digital assets for the current user"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        # Get query parameters
        account_type = request.args.get('type')
        platform = request.args.get('platform')
        
        # Build query
        query = DigitalAsset.query.filter_by(user_id=user.id)
        
        if account_type:
            query = query.filter_by(account_type=account_type)
        
        if platform:
            query = query.filter(DigitalAsset.platform_name.ilike(f'%{platform}%'))
        
        digital_assets = query.order_by(DigitalAsset.updated_at.desc()).all()
        
        # Calculate total value
        total_value = sum(asset.estimated_value or 0 for asset in digital_assets)
        
        return jsonify({
            'digital_assets': [asset.to_dict() for asset in digital_assets],
            'total_value': float(total_value),
            'count': len(digital_assets)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch digital assets', 'details': str(e)}), 500

@digital_assets_bp.route('/<int:asset_id>', methods=['GET'])
def get_digital_asset(asset_id):
    """Get a specific digital asset"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        digital_asset = DigitalAsset.query.filter_by(id=asset_id, user_id=user.id).first()
        if not digital_asset:
            return jsonify({'error': 'Digital asset not found'}), 404
        
        # Include designated contact info
        asset_data = digital_asset.to_dict()
        if digital_asset.designated_contact:
            asset_data['designated_contact'] = digital_asset.designated_contact.to_dict()
        
        # Log access
        log_audit_action(user.id, 'view', 'digital_asset', asset_id, 'Digital asset viewed')
        
        return jsonify({'digital_asset': asset_data}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch digital asset', 'details': str(e)}), 500

@digital_assets_bp.route('/', methods=['POST'])
def create_digital_asset():
    """Create a new digital asset"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.get_json()
        
        # Validate required fields
        if not data.get('platform_name'):
            return jsonify({'error': 'Platform name is required'}), 400
        
        # Verify designated contact if provided
        designated_contact_id = data.get('designated_contact_id')
        if designated_contact_id:
            contact = Beneficiary.query.filter_by(
                id=designated_contact_id,
                user_id=user.id
            ).first()
            if not contact:
                return jsonify({'error': 'Designated contact not found'}), 404
        
        # Create new digital asset
        digital_asset = DigitalAsset(
            user_id=user.id,
            platform_name=data['platform_name'],
            account_type=data.get('account_type'),
            username=data.get('username'),
            email_associated=data.get('email_associated'),
            login_credentials=data.get('login_credentials'),  # Should be encrypted in production
            recovery_codes=data.get('recovery_codes'),  # Should be encrypted in production
            two_factor_backup=data.get('two_factor_backup'),  # Should be encrypted in production
            action_on_death=data.get('action_on_death'),
            special_instructions=data.get('special_instructions'),
            designated_contact_id=designated_contact_id,
            estimated_value=Decimal(str(data['estimated_value'])) if data.get('estimated_value') else None,
            contains_valuable_data=data.get('contains_valuable_data', False)
        )
        
        db.session.add(digital_asset)
        db.session.commit()
        
        # Log creation
        log_audit_action(user.id, 'create', 'digital_asset', digital_asset.id, f'Digital asset created: {digital_asset.platform_name}')
        
        return jsonify({
            'message': 'Digital asset created successfully',
            'digital_asset': digital_asset.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create digital asset', 'details': str(e)}), 500

@digital_assets_bp.route('/<int:asset_id>', methods=['PUT'])
def update_digital_asset(asset_id):
    """Update a digital asset"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        digital_asset = DigitalAsset.query.filter_by(id=asset_id, user_id=user.id).first()
        if not digital_asset:
            return jsonify({'error': 'Digital asset not found'}), 404
        
        data = request.get_json()
        
        # Verify designated contact if provided
        if 'designated_contact_id' in data and data['designated_contact_id']:
            contact = Beneficiary.query.filter_by(
                id=data['designated_contact_id'],
                user_id=user.id
            ).first()
            if not contact:
                return jsonify({'error': 'Designated contact not found'}), 404
        
        # Update fields
        if 'platform_name' in data:
            digital_asset.platform_name = data['platform_name']
        if 'account_type' in data:
            digital_asset.account_type = data['account_type']
        if 'username' in data:
            digital_asset.username = data['username']
        if 'email_associated' in data:
            digital_asset.email_associated = data['email_associated']
        if 'login_credentials' in data:
            digital_asset.login_credentials = data['login_credentials']
        if 'recovery_codes' in data:
            digital_asset.recovery_codes = data['recovery_codes']
        if 'two_factor_backup' in data:
            digital_asset.two_factor_backup = data['two_factor_backup']
        if 'action_on_death' in data:
            digital_asset.action_on_death = data['action_on_death']
        if 'special_instructions' in data:
            digital_asset.special_instructions = data['special_instructions']
        if 'designated_contact_id' in data:
            digital_asset.designated_contact_id = data['designated_contact_id']
        if 'estimated_value' in data:
            digital_asset.estimated_value = Decimal(str(data['estimated_value'])) if data['estimated_value'] else None
        if 'contains_valuable_data' in data:
            digital_asset.contains_valuable_data = data['contains_valuable_data']
        
        digital_asset.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Log update
        log_audit_action(user.id, 'update', 'digital_asset', asset_id, f'Digital asset updated: {digital_asset.platform_name}')
        
        return jsonify({
            'message': 'Digital asset updated successfully',
            'digital_asset': digital_asset.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update digital asset', 'details': str(e)}), 500

@digital_assets_bp.route('/<int:asset_id>', methods=['DELETE'])
def delete_digital_asset(asset_id):
    """Delete a digital asset"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        digital_asset = DigitalAsset.query.filter_by(id=asset_id, user_id=user.id).first()
        if not digital_asset:
            return jsonify({'error': 'Digital asset not found'}), 404
        
        platform_name = digital_asset.platform_name
        
        # Log deletion before deleting
        log_audit_action(user.id, 'delete', 'digital_asset', asset_id, f'Digital asset deleted: {platform_name}')
        
        db.session.delete(digital_asset)
        db.session.commit()
        
        return jsonify({'message': 'Digital asset deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete digital asset', 'details': str(e)}), 500

@digital_assets_bp.route('/summary', methods=['GET'])
def get_digital_assets_summary():
    """Get digital assets summary for the current user"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        digital_assets = DigitalAsset.query.filter_by(user_id=user.id).all()
        
        # Group by account type
        summary = {}
        total_value = 0
        valuable_data_count = 0
        
        for asset in digital_assets:
            account_type = asset.account_type or 'other'
            if account_type not in summary:
                summary[account_type] = {
                    'count': 0,
                    'total_value': 0,
                    'platforms': []
                }
            
            summary[account_type]['count'] += 1
            if asset.estimated_value:
                summary[account_type]['total_value'] += float(asset.estimated_value)
                total_value += float(asset.estimated_value)
            
            if asset.contains_valuable_data:
                valuable_data_count += 1
            
            summary[account_type]['platforms'].append({
                'id': asset.id,
                'platform_name': asset.platform_name,
                'estimated_value': float(asset.estimated_value) if asset.estimated_value else 0,
                'contains_valuable_data': asset.contains_valuable_data
            })
        
        # Count actions on death
        action_counts = {}
        for asset in digital_assets:
            action = asset.action_on_death or 'not_specified'
            action_counts[action] = action_counts.get(action, 0) + 1
        
        return jsonify({
            'summary': summary,
            'total_value': total_value,
            'total_assets': len(digital_assets),
            'valuable_data_count': valuable_data_count,
            'action_counts': action_counts,
            'common_account_types': ['social_media', 'email', 'financial', 'cloud_storage', 'cryptocurrency', 'gaming', 'subscription']
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get digital assets summary', 'details': str(e)}), 500

@digital_assets_bp.route('/platforms', methods=['GET'])
def get_common_platforms():
    """Get list of common digital platforms"""
    try:
        common_platforms = {
            'social_media': [
                'Facebook', 'Instagram', 'Twitter/X', 'LinkedIn', 'TikTok', 'Snapchat', 'YouTube', 'Pinterest'
            ],
            'email': [
                'Gmail', 'Outlook', 'Yahoo Mail', 'iCloud Mail', 'ProtonMail'
            ],
            'financial': [
                'PayPal', 'Venmo', 'Cash App', 'Zelle', 'Coinbase', 'Robinhood', 'E*TRADE'
            ],
            'cloud_storage': [
                'Google Drive', 'Dropbox', 'iCloud', 'OneDrive', 'Box'
            ],
            'cryptocurrency': [
                'Coinbase', 'Binance', 'Kraken', 'MetaMask', 'Hardware Wallet'
            ],
            'subscription': [
                'Netflix', 'Spotify', 'Amazon Prime', 'Adobe Creative Cloud', 'Microsoft 365'
            ],
            'gaming': [
                'Steam', 'PlayStation Network', 'Xbox Live', 'Nintendo Account', 'Epic Games'
            ]
        }
        
        return jsonify({
            'platforms': common_platforms,
            'actions_on_death': [
                'delete', 'memorialize', 'transfer', 'archive', 'maintain', 'contact_platform'
            ]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get platform list', 'details': str(e)}), 500

@digital_assets_bp.route('/test-access/<int:asset_id>', methods=['POST'])
def test_digital_asset_access(asset_id):
    """Test access to a digital asset (simulation)"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        digital_asset = DigitalAsset.query.filter_by(id=asset_id, user_id=user.id).first()
        if not digital_asset:
            return jsonify({'error': 'Digital asset not found'}), 404
        
        # This is a simulation - in a real implementation, this would attempt to verify access
        # For security reasons, we don't actually test real credentials
        
        # Log test access
        log_audit_action(user.id, 'test_access', 'digital_asset', asset_id, f'Access test for: {digital_asset.platform_name}')
        
        # Simulate test results
        test_result = {
            'platform': digital_asset.platform_name,
            'test_status': 'simulated',
            'message': 'Access test simulation completed. In production, this would verify actual credentials.',
            'recommendations': []
        }
        
        # Add recommendations based on asset data
        if not digital_asset.login_credentials:
            test_result['recommendations'].append('Add login credentials for automated access verification')
        
        if not digital_asset.recovery_codes:
            test_result['recommendations'].append('Add recovery codes for account recovery')
        
        if not digital_asset.two_factor_backup:
            test_result['recommendations'].append('Add two-factor authentication backup codes')
        
        if not digital_asset.designated_contact_id:
            test_result['recommendations'].append('Assign a designated contact for this asset')
        
        return jsonify({
            'test_result': test_result,
            'tested_at': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to test digital asset access', 'details': str(e)}), 500

