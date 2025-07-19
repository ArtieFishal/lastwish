from flask import Blueprint, request, jsonify, session
from src.models.user import User, db
from src.models.estate import Beneficiary, RelationshipType, AuditLog
from datetime import datetime

beneficiaries_bp = Blueprint('beneficiaries', __name__)

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

@beneficiaries_bp.route('/', methods=['GET'])
def get_beneficiaries():
    """Get all beneficiaries for the current user"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        # Get query parameters
        relationship = request.args.get('relationship')
        is_primary = request.args.get('is_primary')
        is_contingent = request.args.get('is_contingent')
        is_active = request.args.get('is_active', 'true')
        
        # Build query
        query = Beneficiary.query.filter_by(user_id=user.id)
        
        if relationship:
            try:
                query = query.filter_by(relationship=RelationshipType(relationship))
            except ValueError:
                return jsonify({'error': 'Invalid relationship type'}), 400
        
        if is_primary is not None:
            query = query.filter_by(is_primary=is_primary.lower() == 'true')
        
        if is_contingent is not None:
            query = query.filter_by(is_contingent=is_contingent.lower() == 'true')
        
        if is_active is not None:
            query = query.filter_by(is_active=is_active.lower() == 'true')
        
        beneficiaries = query.order_by(Beneficiary.full_name).all()
        
        return jsonify({
            'beneficiaries': [beneficiary.to_dict() for beneficiary in beneficiaries],
            'count': len(beneficiaries)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch beneficiaries', 'details': str(e)}), 500

@beneficiaries_bp.route('/<int:beneficiary_id>', methods=['GET'])
def get_beneficiary(beneficiary_id):
    """Get a specific beneficiary"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        beneficiary = Beneficiary.query.filter_by(id=beneficiary_id, user_id=user.id).first()
        if not beneficiary:
            return jsonify({'error': 'Beneficiary not found'}), 404
        
        # Include related information
        beneficiary_data = beneficiary.to_dict()
        
        # Add asset distributions
        beneficiary_data['asset_distributions'] = [
            {
                'distribution': dist.to_dict(),
                'asset': dist.asset.to_dict()
            }
            for dist in beneficiary.asset_distributions
        ]
        
        # Add roles (executor, guardian, etc.)
        beneficiary_data['roles'] = {
            'executor_wills': len(beneficiary.executor_wills),
            'alt_executor_wills': len(beneficiary.alt_executor_wills),
            'guardian_wills': len(beneficiary.guardian_wills),
            'alt_guardian_wills': len(beneficiary.alt_guardian_wills),
            'poa_agent_docs': len(beneficiary.poa_agent_docs),
            'healthcare_agent_docs': len(beneficiary.healthcare_agent_docs)
        }
        
        # Log access
        log_audit_action(user.id, 'view', 'beneficiary', beneficiary_id, 'Beneficiary viewed')
        
        return jsonify({'beneficiary': beneficiary_data}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch beneficiary', 'details': str(e)}), 500

@beneficiaries_bp.route('/', methods=['POST'])
def create_beneficiary():
    """Create a new beneficiary"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.get_json()
        
        # Validate required fields
        if not data.get('full_name') or not data.get('relationship'):
            return jsonify({'error': 'Full name and relationship are required'}), 400
        
        try:
            relationship = RelationshipType(data['relationship'])
        except ValueError:
            return jsonify({'error': 'Invalid relationship type'}), 400
        
        # Create new beneficiary
        beneficiary = Beneficiary(
            user_id=user.id,
            full_name=data['full_name'],
            relationship=relationship,
            email=data.get('email'),
            phone=data.get('phone'),
            address=data.get('address'),
            date_of_birth=datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date() if data.get('date_of_birth') else None,
            ssn_last_four=data.get('ssn_last_four'),
            organization_name=data.get('organization_name'),
            tax_id=data.get('tax_id'),
            is_primary=data.get('is_primary', True),
            is_contingent=data.get('is_contingent', False),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(beneficiary)
        db.session.commit()
        
        # Log creation
        log_audit_action(user.id, 'create', 'beneficiary', beneficiary.id, f'Beneficiary created: {beneficiary.full_name}')
        
        return jsonify({
            'message': 'Beneficiary created successfully',
            'beneficiary': beneficiary.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create beneficiary', 'details': str(e)}), 500

@beneficiaries_bp.route('/<int:beneficiary_id>', methods=['PUT'])
def update_beneficiary(beneficiary_id):
    """Update a beneficiary"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        beneficiary = Beneficiary.query.filter_by(id=beneficiary_id, user_id=user.id).first()
        if not beneficiary:
            return jsonify({'error': 'Beneficiary not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'full_name' in data:
            beneficiary.full_name = data['full_name']
        if 'relationship' in data:
            try:
                beneficiary.relationship = RelationshipType(data['relationship'])
            except ValueError:
                return jsonify({'error': 'Invalid relationship type'}), 400
        if 'email' in data:
            beneficiary.email = data['email']
        if 'phone' in data:
            beneficiary.phone = data['phone']
        if 'address' in data:
            beneficiary.address = data['address']
        if 'date_of_birth' in data:
            beneficiary.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date() if data['date_of_birth'] else None
        if 'ssn_last_four' in data:
            beneficiary.ssn_last_four = data['ssn_last_four']
        if 'organization_name' in data:
            beneficiary.organization_name = data['organization_name']
        if 'tax_id' in data:
            beneficiary.tax_id = data['tax_id']
        if 'is_primary' in data:
            beneficiary.is_primary = data['is_primary']
        if 'is_contingent' in data:
            beneficiary.is_contingent = data['is_contingent']
        if 'is_active' in data:
            beneficiary.is_active = data['is_active']
        
        beneficiary.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Log update
        log_audit_action(user.id, 'update', 'beneficiary', beneficiary_id, f'Beneficiary updated: {beneficiary.full_name}')
        
        return jsonify({
            'message': 'Beneficiary updated successfully',
            'beneficiary': beneficiary.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update beneficiary', 'details': str(e)}), 500

@beneficiaries_bp.route('/<int:beneficiary_id>', methods=['DELETE'])
def delete_beneficiary(beneficiary_id):
    """Delete a beneficiary"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        beneficiary = Beneficiary.query.filter_by(id=beneficiary_id, user_id=user.id).first()
        if not beneficiary:
            return jsonify({'error': 'Beneficiary not found'}), 404
        
        # Check if beneficiary is referenced in any distributions or roles
        if (beneficiary.asset_distributions or 
            beneficiary.executor_wills or 
            beneficiary.alt_executor_wills or 
            beneficiary.guardian_wills or 
            beneficiary.alt_guardian_wills or
            beneficiary.poa_agent_docs or
            beneficiary.healthcare_agent_docs):
            return jsonify({
                'error': 'Cannot delete beneficiary with existing distributions or roles',
                'suggestion': 'Consider deactivating instead of deleting'
            }), 400
        
        beneficiary_name = beneficiary.full_name
        
        # Log deletion before deleting
        log_audit_action(user.id, 'delete', 'beneficiary', beneficiary_id, f'Beneficiary deleted: {beneficiary_name}')
        
        db.session.delete(beneficiary)
        db.session.commit()
        
        return jsonify({'message': 'Beneficiary deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete beneficiary', 'details': str(e)}), 500

@beneficiaries_bp.route('/<int:beneficiary_id>/deactivate', methods=['POST'])
def deactivate_beneficiary(beneficiary_id):
    """Deactivate a beneficiary (soft delete)"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        beneficiary = Beneficiary.query.filter_by(id=beneficiary_id, user_id=user.id).first()
        if not beneficiary:
            return jsonify({'error': 'Beneficiary not found'}), 404
        
        beneficiary.is_active = False
        beneficiary.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Log deactivation
        log_audit_action(user.id, 'deactivate', 'beneficiary', beneficiary_id, f'Beneficiary deactivated: {beneficiary.full_name}')
        
        return jsonify({
            'message': 'Beneficiary deactivated successfully',
            'beneficiary': beneficiary.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to deactivate beneficiary', 'details': str(e)}), 500

@beneficiaries_bp.route('/<int:beneficiary_id>/activate', methods=['POST'])
def activate_beneficiary(beneficiary_id):
    """Activate a beneficiary"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        beneficiary = Beneficiary.query.filter_by(id=beneficiary_id, user_id=user.id).first()
        if not beneficiary:
            return jsonify({'error': 'Beneficiary not found'}), 404
        
        beneficiary.is_active = True
        beneficiary.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Log activation
        log_audit_action(user.id, 'activate', 'beneficiary', beneficiary_id, f'Beneficiary activated: {beneficiary.full_name}')
        
        return jsonify({
            'message': 'Beneficiary activated successfully',
            'beneficiary': beneficiary.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to activate beneficiary', 'details': str(e)}), 500

@beneficiaries_bp.route('/summary', methods=['GET'])
def get_beneficiaries_summary():
    """Get beneficiaries summary for the current user"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        beneficiaries = Beneficiary.query.filter_by(user_id=user.id, is_active=True).all()
        
        # Group by relationship
        summary = {}
        for beneficiary in beneficiaries:
            relationship = beneficiary.relationship.value
            if relationship not in summary:
                summary[relationship] = {
                    'count': 0,
                    'primary': 0,
                    'contingent': 0,
                    'beneficiaries': []
                }
            
            summary[relationship]['count'] += 1
            if beneficiary.is_primary:
                summary[relationship]['primary'] += 1
            if beneficiary.is_contingent:
                summary[relationship]['contingent'] += 1
            
            summary[relationship]['beneficiaries'].append({
                'id': beneficiary.id,
                'full_name': beneficiary.full_name,
                'is_primary': beneficiary.is_primary,
                'is_contingent': beneficiary.is_contingent
            })
        
        # Count roles
        executor_count = len([b for b in beneficiaries if b.executor_wills])
        guardian_count = len([b for b in beneficiaries if b.guardian_wills])
        poa_agent_count = len([b for b in beneficiaries if b.poa_agent_docs])
        healthcare_agent_count = len([b for b in beneficiaries if b.healthcare_agent_docs])
        
        return jsonify({
            'summary': summary,
            'total_beneficiaries': len(beneficiaries),
            'roles': {
                'executors': executor_count,
                'guardians': guardian_count,
                'poa_agents': poa_agent_count,
                'healthcare_agents': healthcare_agent_count
            },
            'relationship_types': [rel_type.value for rel_type in RelationshipType]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get beneficiaries summary', 'details': str(e)}), 500

@beneficiaries_bp.route('/search', methods=['GET'])
def search_beneficiaries():
    """Search beneficiaries by name or email"""
    try:
        user = require_auth()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        query_param = request.args.get('q', '').strip()
        if not query_param:
            return jsonify({'error': 'Search query is required'}), 400
        
        # Search by name or email
        beneficiaries = Beneficiary.query.filter(
            Beneficiary.user_id == user.id,
            Beneficiary.is_active == True,
            (Beneficiary.full_name.ilike(f'%{query_param}%') |
             Beneficiary.email.ilike(f'%{query_param}%'))
        ).order_by(Beneficiary.full_name).all()
        
        return jsonify({
            'beneficiaries': [beneficiary.to_dict() for beneficiary in beneficiaries],
            'count': len(beneficiaries),
            'query': query_param
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to search beneficiaries', 'details': str(e)}), 500

