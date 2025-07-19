from flask import Blueprint, request, jsonify, session
from src.models.user import User, db
from src.models.estate import Will, Beneficiary, DocumentStatus, AuditLog
from datetime import datetime, date

will_bp = Blueprint('will', __name__)

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

@will_bp.route('/', methods=['GET'])
def get_wills():
    """Get all wills for the current user"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        wills = Will.query.filter_by(user_id=user.id).order_by(Will.updated_at.desc()).all()
        
        return jsonify({
            'wills': [will.to_dict() for will in wills]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch wills', 'details': str(e)}), 500

@will_bp.route('/<int:will_id>', methods=['GET'])
def get_will(will_id):
    """Get a specific will"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        will = Will.query.filter_by(id=will_id, user_id=user.id).first()
        if not will:
            return jsonify({'error': 'Will not found'}), 404
        
        # Log access
        log_audit_action(user.id, 'view', 'will', will_id, 'Will viewed')
        
        return jsonify({'will': will.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch will', 'details': str(e)}), 500

@will_bp.route('/', methods=['POST'])
def create_will():
    """Create a new will"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.get_json()
        
        # Create new will
        will = Will(
            user_id=user.id,
            title=data.get('title', 'Last Will and Testament'),
            testator_full_name=data.get('testator_full_name', user.full_name),
            testator_address=data.get('testator_address', user.full_address),
            testator_date_of_birth=datetime.strptime(data['testator_date_of_birth'], '%Y-%m-%d').date() if data.get('testator_date_of_birth') else user.date_of_birth,
            testator_ssn_last_four=data.get('testator_ssn_last_four', user.ssn_last_four),
            status=DocumentStatus.DRAFT
        )
        
        db.session.add(will)
        db.session.commit()
        
        # Log creation
        log_audit_action(user.id, 'create', 'will', will.id, 'Will created')
        
        return jsonify({
            'message': 'Will created successfully',
            'will': will.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create will', 'details': str(e)}), 500

@will_bp.route('/<int:will_id>', methods=['PUT'])
def update_will(will_id):
    """Update a will"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        will = Will.query.filter_by(id=will_id, user_id=user.id).first()
        if not will:
            return jsonify({'error': 'Will not found'}), 404
        
        # Check if will is already executed
        if will.status == DocumentStatus.EXECUTED:
            return jsonify({'error': 'Cannot modify executed will'}), 400
        
        data = request.get_json()
        
        # Update fields
        if 'title' in data:
            will.title = data['title']
        if 'testator_full_name' in data:
            will.testator_full_name = data['testator_full_name']
        if 'testator_address' in data:
            will.testator_address = data['testator_address']
        if 'testator_date_of_birth' in data:
            will.testator_date_of_birth = datetime.strptime(data['testator_date_of_birth'], '%Y-%m-%d').date()
        if 'testator_ssn_last_four' in data:
            will.testator_ssn_last_four = data['testator_ssn_last_four']
        if 'executor_id' in data:
            will.executor_id = data['executor_id']
        if 'alternate_executor_id' in data:
            will.alternate_executor_id = data['alternate_executor_id']
        if 'guardian_id' in data:
            will.guardian_id = data['guardian_id']
        if 'alternate_guardian_id' in data:
            will.alternate_guardian_id = data['alternate_guardian_id']
        if 'funeral_instructions' in data:
            will.funeral_instructions = data['funeral_instructions']
        if 'burial_instructions' in data:
            will.burial_instructions = data['burial_instructions']
        if 'special_instructions' in data:
            will.special_instructions = data['special_instructions']
        if 'status' in data:
            will.status = DocumentStatus(data['status'])
        
        will.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Log update
        log_audit_action(user.id, 'update', 'will', will_id, 'Will updated')
        
        return jsonify({
            'message': 'Will updated successfully',
            'will': will.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update will', 'details': str(e)}), 500

@will_bp.route('/<int:will_id>', methods=['DELETE'])
def delete_will(will_id):
    """Delete a will"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        will = Will.query.filter_by(id=will_id, user_id=user.id).first()
        if not will:
            return jsonify({'error': 'Will not found'}), 404
        
        # Check if will is executed
        if will.status == DocumentStatus.EXECUTED:
            return jsonify({'error': 'Cannot delete executed will'}), 400
        
        # Log deletion before deleting
        log_audit_action(user.id, 'delete', 'will', will_id, 'Will deleted')
        
        db.session.delete(will)
        db.session.commit()
        
        return jsonify({'message': 'Will deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete will', 'details': str(e)}), 500

@will_bp.route('/<int:will_id>/execute', methods=['POST'])
def execute_will(will_id):
    """Execute a will (mark as legally executed)"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        will = Will.query.filter_by(id=will_id, user_id=user.id).first()
        if not will:
            return jsonify({'error': 'Will not found'}), 404
        
        if will.status == DocumentStatus.EXECUTED:
            return jsonify({'error': 'Will is already executed'}), 400
        
        data = request.get_json()
        
        # Update execution information
        will.status = DocumentStatus.EXECUTED
        will.executed_at = datetime.utcnow()
        
        # Store digital signatures
        if 'testator_signature' in data:
            will.testator_signature = data['testator_signature']
        if 'witness_1_signature' in data:
            will.witness_1_signature = data['witness_1_signature']
        if 'witness_2_signature' in data:
            will.witness_2_signature = data['witness_2_signature']
        if 'notary_signature' in data:
            will.notary_signature = data['notary_signature']
        
        will.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Log execution
        log_audit_action(user.id, 'execute', 'will', will_id, 'Will executed legally')
        
        return jsonify({
            'message': 'Will executed successfully',
            'will': will.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to execute will', 'details': str(e)}), 500

@will_bp.route('/<int:will_id>/status', methods=['GET'])
def get_will_status(will_id):
    """Get will completion status"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        will = Will.query.filter_by(id=will_id, user_id=user.id).first()
        if not will:
            return jsonify({'error': 'Will not found'}), 404
        
        # Calculate completion percentage
        completion_items = {
            'personal_info': bool(will.testator_full_name and will.testator_address),
            'executor': bool(will.executor_id),
            'assets': len(will.assets) > 0,
            'beneficiaries': len([asset for asset in will.assets if asset.distributions]) > 0,
            'instructions': bool(will.funeral_instructions or will.burial_instructions)
        }
        
        completed_count = sum(completion_items.values())
        total_count = len(completion_items)
        completion_percentage = (completed_count / total_count) * 100
        
        return jsonify({
            'will_id': will_id,
            'status': will.status.value,
            'completion_percentage': completion_percentage,
            'completion_items': completion_items,
            'is_ready_for_execution': completion_percentage >= 80 and will.status != DocumentStatus.EXECUTED
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get will status', 'details': str(e)}), 500

@will_bp.route('/<int:will_id>/preview', methods=['GET'])
def preview_will(will_id):
    """Generate a preview of the will document"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        will = Will.query.filter_by(id=will_id, user_id=user.id).first()
        if not will:
            return jsonify({'error': 'Will not found'}), 404
        
        # Log preview access
        log_audit_action(user.id, 'preview', 'will', will_id, 'Will preview generated')
        
        # Generate will preview data
        preview_data = {
            'will': will.to_dict(),
            'testator': user.to_dict(),
            'executor': will.executor.to_dict() if will.executor else None,
            'alternate_executor': will.alternate_executor.to_dict() if will.alternate_executor else None,
            'guardian': will.guardian.to_dict() if will.guardian else None,
            'alternate_guardian': will.alternate_guardian.to_dict() if will.alternate_guardian else None,
            'assets': [asset.to_dict() for asset in will.assets],
            'asset_distributions': []
        }
        
        # Add asset distributions
        for asset in will.assets:
            for distribution in asset.distributions:
                preview_data['asset_distributions'].append({
                    'asset': asset.to_dict(),
                    'distribution': distribution.to_dict(),
                    'beneficiary': distribution.beneficiary.to_dict()
                })
        
        return jsonify({
            'preview': preview_data,
            'generated_at': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to generate will preview', 'details': str(e)}), 500

