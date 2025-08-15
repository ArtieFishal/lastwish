from flask import Blueprint, request, jsonify, session
from src.models.user import User, db
from src.models.estate import Asset, AssetDistribution, AssetType, Beneficiary, AuditLog
from datetime import datetime
from decimal import Decimal

assets_bp = Blueprint('assets', __name__)

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

@assets_bp.route('/', methods=['GET'])
def get_assets():
    """Get all assets for the current user"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        # Get query parameters
        asset_type = request.args.get('type')
        will_id = request.args.get('will_id')
        
        # Build query
        query = Asset.query.filter_by(user_id=user.id)
        
        if asset_type:
            try:
                query = query.filter_by(asset_type=AssetType(asset_type))
            except ValueError:
                return jsonify({'error': 'Invalid asset type'}), 400
        
        if will_id:
            query = query.filter_by(will_id=will_id)
        
        assets = query.order_by(Asset.updated_at.desc()).all()
        
        # Calculate total value
        total_value = sum(asset.estimated_value or 0 for asset in assets)
        
        return jsonify({
            'assets': [asset.to_dict() for asset in assets],
            'total_value': float(total_value),
            'count': len(assets)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch assets', 'details': str(e)}), 500

@assets_bp.route('/<int:asset_id>', methods=['GET'])
def get_asset(asset_id):
    """Get a specific asset"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        asset = Asset.query.filter_by(id=asset_id, user_id=user.id).first()
        if not asset:
            return jsonify({'error': 'Asset not found'}), 404
        
        # Include distributions
        asset_data = asset.to_dict()
        asset_data['distributions'] = [
            {
                'distribution': dist.to_dict(),
                'beneficiary': dist.beneficiary.to_dict()
            }
            for dist in asset.distributions
        ]
        
        # Log access
        log_audit_action(user.id, 'view', 'asset', asset_id, 'Asset viewed')
        
        return jsonify({'asset': asset_data}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch asset', 'details': str(e)}), 500

@assets_bp.route('/', methods=['POST'])
def create_asset():
    """Create a new asset"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name') or not data.get('asset_type'):
            return jsonify({'error': 'Name and asset type are required'}), 400
        
        try:
            asset_type = AssetType(data['asset_type'])
        except ValueError:
            return jsonify({'error': 'Invalid asset type'}), 400
        
        # Create new asset
        asset = Asset(
            user_id=user.id,
            will_id=data.get('will_id'),
            name=data['name'],
            asset_type=asset_type,
            description=data.get('description'),
            estimated_value=Decimal(str(data['estimated_value'])) if data.get('estimated_value') else None,
            location=data.get('location'),
            institution_name=data.get('institution_name'),
            account_number=data.get('account_number'),
            deed_title_info=data.get('deed_title_info'),
            liens_mortgages=data.get('liens_mortgages'),
            login_credentials=data.get('login_credentials'),  # Should be encrypted in production
            recovery_information=data.get('recovery_information')  # Should be encrypted in production
        )
        
        db.session.add(asset)
        db.session.commit()
        
        # Log creation
        log_audit_action(user.id, 'create', 'asset', asset.id, f'Asset created: {asset.name}')
        
        return jsonify({
            'message': 'Asset created successfully',
            'asset': asset.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create asset', 'details': str(e)}), 500

@assets_bp.route('/<int:asset_id>', methods=['PUT'])
def update_asset(asset_id):
    """Update an asset"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        asset = Asset.query.filter_by(id=asset_id, user_id=user.id).first()
        if not asset:
            return jsonify({'error': 'Asset not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'name' in data:
            asset.name = data['name']
        if 'asset_type' in data:
            try:
                asset.asset_type = AssetType(data['asset_type'])
            except ValueError:
                return jsonify({'error': 'Invalid asset type'}), 400
        if 'description' in data:
            asset.description = data['description']
        if 'estimated_value' in data:
            asset.estimated_value = Decimal(str(data['estimated_value'])) if data['estimated_value'] else None
        if 'location' in data:
            asset.location = data['location']
        if 'institution_name' in data:
            asset.institution_name = data['institution_name']
        if 'account_number' in data:
            asset.account_number = data['account_number']
        if 'deed_title_info' in data:
            asset.deed_title_info = data['deed_title_info']
        if 'liens_mortgages' in data:
            asset.liens_mortgages = data['liens_mortgages']
        if 'login_credentials' in data:
            asset.login_credentials = data['login_credentials']
        if 'recovery_information' in data:
            asset.recovery_information = data['recovery_information']
        if 'will_id' in data:
            asset.will_id = data['will_id']
        
        asset.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Log update
        log_audit_action(user.id, 'update', 'asset', asset_id, f'Asset updated: {asset.name}')
        
        return jsonify({
            'message': 'Asset updated successfully',
            'asset': asset.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update asset', 'details': str(e)}), 500

@assets_bp.route('/<int:asset_id>', methods=['DELETE'])
def delete_asset(asset_id):
    """Delete an asset"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        asset = Asset.query.filter_by(id=asset_id, user_id=user.id).first()
        if not asset:
            return jsonify({'error': 'Asset not found'}), 404
        
        asset_name = asset.name
        
        # Log deletion before deleting
        log_audit_action(user.id, 'delete', 'asset', asset_id, f'Asset deleted: {asset_name}')
        
        db.session.delete(asset)
        db.session.commit()
        
        return jsonify({'message': 'Asset deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete asset', 'details': str(e)}), 500

@assets_bp.route('/<int:asset_id>/distributions', methods=['GET'])
def get_asset_distributions(asset_id):
    """Get distributions for a specific asset"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        asset = Asset.query.filter_by(id=asset_id, user_id=user.id).first()
        if not asset:
            return jsonify({'error': 'Asset not found'}), 404
        
        distributions = AssetDistribution.query.filter_by(asset_id=asset_id).all()
        
        distribution_data = []
        for dist in distributions:
            distribution_data.append({
                'distribution': dist.to_dict(),
                'beneficiary': dist.beneficiary.to_dict()
            })
        
        return jsonify({
            'asset': asset.to_dict(),
            'distributions': distribution_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch asset distributions', 'details': str(e)}), 500

@assets_bp.route('/<int:asset_id>/distributions', methods=['POST'])
def create_asset_distribution(asset_id):
    """Create a new asset distribution"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        asset = Asset.query.filter_by(id=asset_id, user_id=user.id).first()
        if not asset:
            return jsonify({'error': 'Asset not found'}), 404
        
        data = request.get_json()
        
        # Validate required fields
        if not data.get('beneficiary_id'):
            return jsonify({'error': 'Beneficiary ID is required'}), 400
        
        # Verify beneficiary belongs to user
        beneficiary = Beneficiary.query.filter_by(
            id=data['beneficiary_id'],
            user_id=user.id
        ).first()
        if not beneficiary:
            return jsonify({'error': 'Beneficiary not found'}), 404
        
        # Validate percentage or amount
        if not data.get('percentage') and not data.get('specific_amount'):
            return jsonify({'error': 'Either percentage or specific amount is required'}), 400
        
        # Create distribution
        distribution = AssetDistribution(
            asset_id=asset_id,
            beneficiary_id=data['beneficiary_id'],
            percentage=Decimal(str(data['percentage'])) if data.get('percentage') else None,
            specific_amount=Decimal(str(data['specific_amount'])) if data.get('specific_amount') else None,
            conditions=data.get('conditions'),
            is_primary=data.get('is_primary', True),
            is_contingent=data.get('is_contingent', False)
        )
        
        db.session.add(distribution)
        db.session.commit()
        
        # Log creation
        log_audit_action(
            user.id, 'create', 'asset_distribution', distribution.id,
            f'Distribution created for asset: {asset.name} to {beneficiary.full_name}'
        )
        
        return jsonify({
            'message': 'Asset distribution created successfully',
            'distribution': distribution.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create asset distribution', 'details': str(e)}), 500

@assets_bp.route('/<int:asset_id>/distributions/<int:distribution_id>', methods=['PUT'])
def update_asset_distribution(asset_id, distribution_id):
    """Update an asset distribution"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        # Verify asset belongs to user
        asset = Asset.query.filter_by(id=asset_id, user_id=user.id).first()
        if not asset:
            return jsonify({'error': 'Asset not found'}), 404
        
        distribution = AssetDistribution.query.filter_by(
            id=distribution_id,
            asset_id=asset_id
        ).first()
        if not distribution:
            return jsonify({'error': 'Distribution not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'beneficiary_id' in data:
            # Verify new beneficiary belongs to user
            beneficiary = Beneficiary.query.filter_by(
                id=data['beneficiary_id'],
                user_id=user.id
            ).first()
            if not beneficiary:
                return jsonify({'error': 'Beneficiary not found'}), 404
            distribution.beneficiary_id = data['beneficiary_id']
        
        if 'percentage' in data:
            distribution.percentage = Decimal(str(data['percentage'])) if data['percentage'] else None
        if 'specific_amount' in data:
            distribution.specific_amount = Decimal(str(data['specific_amount'])) if data['specific_amount'] else None
        if 'conditions' in data:
            distribution.conditions = data['conditions']
        if 'is_primary' in data:
            distribution.is_primary = data['is_primary']
        if 'is_contingent' in data:
            distribution.is_contingent = data['is_contingent']
        
        db.session.commit()
        
        # Log update
        log_audit_action(
            user.id, 'update', 'asset_distribution', distribution_id,
            f'Distribution updated for asset: {asset.name}'
        )
        
        return jsonify({
            'message': 'Asset distribution updated successfully',
            'distribution': distribution.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update asset distribution', 'details': str(e)}), 500

@assets_bp.route('/<int:asset_id>/distributions/<int:distribution_id>', methods=['DELETE'])
def delete_asset_distribution(asset_id, distribution_id):
    """Delete an asset distribution"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        # Verify asset belongs to user
        asset = Asset.query.filter_by(id=asset_id, user_id=user.id).first()
        if not asset:
            return jsonify({'error': 'Asset not found'}), 404
        
        distribution = AssetDistribution.query.filter_by(
            id=distribution_id,
            asset_id=asset_id
        ).first()
        if not distribution:
            return jsonify({'error': 'Distribution not found'}), 404
        
        # Log deletion before deleting
        log_audit_action(
            user.id, 'delete', 'asset_distribution', distribution_id,
            f'Distribution deleted for asset: {asset.name}'
        )
        
        db.session.delete(distribution)
        db.session.commit()
        
        return jsonify({'message': 'Asset distribution deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete asset distribution', 'details': str(e)}), 500

@assets_bp.route('/summary', methods=['GET'])
def get_assets_summary():
    """Get assets summary for the current user"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        assets = Asset.query.filter_by(user_id=user.id).all()
        
        # Group by asset type
        summary = {}
        total_value = 0
        
        for asset in assets:
            asset_type = asset.asset_type.value
            if asset_type not in summary:
                summary[asset_type] = {
                    'count': 0,
                    'total_value': 0,
                    'assets': []
                }
            
            summary[asset_type]['count'] += 1
            if asset.estimated_value:
                summary[asset_type]['total_value'] += float(asset.estimated_value)
                total_value += float(asset.estimated_value)
            
            summary[asset_type]['assets'].append({
                'id': asset.id,
                'name': asset.name,
                'estimated_value': float(asset.estimated_value) if asset.estimated_value else 0
            })
        
        # Count distributions
        total_distributions = AssetDistribution.query.join(Asset).filter(
            Asset.user_id == user.id
        ).count()
        
        return jsonify({
            'summary': summary,
            'total_value': total_value,
            'total_assets': len(assets),
            'total_distributions': total_distributions,
            'asset_types': [asset_type.value for asset_type in AssetType]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get assets summary', 'details': str(e)}), 500

