"""
Legal Routes for Last Wish Platform
Handles legal document templates, state requirements, and compliance checking
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User
from src.models.addendum import Addendum
from src.models.legal_template import LegalTemplate, StateRequirement, ComplianceCheck, LegalResource
from src.services.legal_service import LegalService
from src.models.user import db

legal_bp = Blueprint('legal', __name__)
legal_service = LegalService()

@legal_bp.route('/templates', methods=['GET'])
@jwt_required()
def get_legal_templates():
    """Get available legal document templates"""
    try:
        template_type = request.args.get('type')
        state_code = request.args.get('state')
        
        templates = legal_service.get_legal_templates(template_type, state_code)
        
        return jsonify({
            'success': True,
            'templates': templates,
            'count': len(templates)
        })
    except Exception as e:
        current_app.logger.error(f"Error getting legal templates: {e}")
        return jsonify({'error': 'Failed to retrieve legal templates'}), 500

@legal_bp.route('/templates/<int:template_id>', methods=['GET'])
@jwt_required()
def get_legal_template(template_id):
    """Get a specific legal template"""
    try:
        template = LegalTemplate.query.get(template_id)
        if not template or not template.is_active:
            return jsonify({'error': 'Template not found'}), 404
        
        return jsonify({
            'success': True,
            'template': template.to_dict()
        })
    except Exception as e:
        current_app.logger.error(f"Error getting legal template: {e}")
        return jsonify({'error': 'Failed to retrieve template'}), 500

@legal_bp.route('/generate-document', methods=['POST'])
@jwt_required()
def generate_document():
    """Generate a legal document from template"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        template_id = data.get('template_id')
        addendum_id = data.get('addendum_id')
        
        if not template_id:
            return jsonify({'error': 'Template ID is required'}), 400
        
        # Get user data
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user_data = {
            'full_name': user.full_name,
            'address': user.address,
            'city': user.city,
            'state': user.state,
            'zip_code': user.zip_code,
            'date_of_birth': user.date_of_birth.isoformat() if user.date_of_birth else None
        }
        
        # Get addendum data if provided
        addendum_data = {}
        if addendum_id:
            addendum = Addendum.query.filter_by(id=addendum_id, user_id=user_id).first()
            if addendum:
                addendum_data = {
                    'title': addendum.title,
                    'assets': addendum.assets,
                    'beneficiaries': addendum.beneficiaries,
                    'instructions': addendum.instructions
                }
        
        # Generate document
        result = legal_service.generate_document(template_id, user_data, addendum_data)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify({
            'success': True,
            'document': result
        })
    except Exception as e:
        current_app.logger.error(f"Error generating document: {e}")
        return jsonify({'error': 'Failed to generate document'}), 500

@legal_bp.route('/state-requirements/<state_code>', methods=['GET'])
@jwt_required()
def get_state_requirements(state_code):
    """Get legal requirements for a specific state"""
    try:
        requirements = legal_service.get_state_requirements(state_code)
        
        if not requirements:
            return jsonify({'error': 'State requirements not found'}), 404
        
        return jsonify({
            'success': True,
            'requirements': requirements
        })
    except Exception as e:
        current_app.logger.error(f"Error getting state requirements: {e}")
        return jsonify({'error': 'Failed to retrieve state requirements'}), 500

@legal_bp.route('/compliance-check', methods=['POST'])
@jwt_required()
def check_compliance():
    """Perform compliance check for user's documents"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        addendum_id = data.get('addendum_id')
        state_code = data.get('state_code')
        
        result = legal_service.check_compliance(user_id, addendum_id, state_code)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify({
            'success': True,
            'compliance_check': result
        })
    except Exception as e:
        current_app.logger.error(f"Error checking compliance: {e}")
        return jsonify({'error': 'Failed to perform compliance check'}), 500

@legal_bp.route('/compliance-history', methods=['GET'])
@jwt_required()
def get_compliance_history():
    """Get user's compliance check history"""
    try:
        user_id = get_jwt_identity()
        
        checks = ComplianceCheck.query.filter_by(user_id=user_id).order_by(ComplianceCheck.checked_at.desc()).all()
        
        return jsonify({
            'success': True,
            'compliance_checks': [check.to_dict() for check in checks],
            'count': len(checks)
        })
    except Exception as e:
        current_app.logger.error(f"Error getting compliance history: {e}")
        return jsonify({'error': 'Failed to retrieve compliance history'}), 500

@legal_bp.route('/resources', methods=['GET'])
@jwt_required()
def get_legal_resources():
    """Get legal resources and educational content"""
    try:
        category = request.args.get('category')
        state_code = request.args.get('state')
        audience = request.args.get('audience')
        
        resources = legal_service.get_legal_resources(category, state_code, audience)
        
        return jsonify({
            'success': True,
            'resources': resources,
            'count': len(resources)
        })
    except Exception as e:
        current_app.logger.error(f"Error getting legal resources: {e}")
        return jsonify({'error': 'Failed to retrieve legal resources'}), 500

@legal_bp.route('/validate-document', methods=['POST'])
@jwt_required()
def validate_document():
    """Validate document content"""
    try:
        data = request.get_json()
        
        content = data.get('content')
        template_type = data.get('template_type', 'will_addendum')
        
        if not content:
            return jsonify({'error': 'Document content is required'}), 400
        
        result = legal_service.validate_document_content(content, template_type)
        
        return jsonify({
            'success': True,
            'validation': result
        })
    except Exception as e:
        current_app.logger.error(f"Error validating document: {e}")
        return jsonify({'error': 'Failed to validate document'}), 500

@legal_bp.route('/notary-requirements/<state_code>', methods=['GET'])
@jwt_required()
def get_notary_requirements(state_code):
    """Get notarization requirements for a state"""
    try:
        requirements = legal_service.get_notary_requirements(state_code)
        
        if 'error' in requirements:
            return jsonify(requirements), 404
        
        return jsonify({
            'success': True,
            'notary_requirements': requirements
        })
    except Exception as e:
        current_app.logger.error(f"Error getting notary requirements: {e}")
        return jsonify({'error': 'Failed to retrieve notary requirements'}), 500

@legal_bp.route('/states', methods=['GET'])
@jwt_required()
def get_all_states():
    """Get all states with their basic requirements"""
    try:
        states = StateRequirement.query.all()
        
        return jsonify({
            'success': True,
            'states': [state.to_dict() for state in states],
            'count': len(states)
        })
    except Exception as e:
        current_app.logger.error(f"Error getting states: {e}")
        return jsonify({'error': 'Failed to retrieve states'}), 500

@legal_bp.route('/faq', methods=['GET'])
@jwt_required()
def get_legal_faq():
    """Get frequently asked legal questions"""
    try:
        category = request.args.get('category', 'estate_planning')
        
        faqs = legal_service.get_legal_resources(category='faq', audience='general')
        
        return jsonify({
            'success': True,
            'faqs': faqs,
            'count': len(faqs)
        })
    except Exception as e:
        current_app.logger.error(f"Error getting legal FAQ: {e}")
        return jsonify({'error': 'Failed to retrieve FAQ'}), 500

# Legacy endpoints for backward compatibility
@legal_bp.route('/notarization-guide', methods=['GET'])
def get_notarization_guide():
    """Get notarization guide (legacy endpoint)"""
    try:
        state = request.args.get('state', 'general')
        
        guide = {
            'general_requirements': [
                'Valid government-issued photo identification',
                'Unsigned document (sign in presence of notary)',
                'Understanding of document contents',
                'Voluntary signing (no coercion)'
            ],
            'process': [
                'Contact a licensed notary public',
                'Bring valid ID and unsigned document',
                'Verify your identity with the notary',
                'Sign the document in the notary\'s presence',
                'Notary completes the acknowledgment',
                'Pay notary fee (typically $5-15)'
            ],
            'finding_notaries': [
                'Banks and credit unions',
                'UPS stores and shipping centers',
                'Law offices',
                'Real estate offices',
                'Online notary services (where permitted)'
            ],
            'tips': [
                'Call ahead to confirm notary availability',
                'Bring multiple forms of ID if possible',
                'Don\'t sign the document beforehand',
                'Ask about witness requirements in your state',
                'Keep the notarized original in a safe place'
            ]
        }
        
        return jsonify({'guide': guide}), 200
        
    except Exception as e:
        current_app.logger.error(f"Get notarization guide error: {str(e)}")
        return jsonify({'error': 'Failed to get notarization guide'}), 500

@legal_bp.route('/jurisdictions', methods=['GET'])
def get_supported_jurisdictions():
    """Get supported jurisdictions (legacy endpoint)"""
    jurisdictions = [
        {
            'code': 'general',
            'name': 'General (All States)',
            'description': 'General template compliant with Uniform Probate Code'
        },
        {
            'code': 'CA',
            'name': 'California',
            'description': 'California-specific requirements'
        },
        {
            'code': 'NY',
            'name': 'New York',
            'description': 'New York-specific requirements'
        },
        {
            'code': 'TX',
            'name': 'Texas',
            'description': 'Texas-specific requirements'
        },
        {
            'code': 'FL',
            'name': 'Florida',
            'description': 'Florida-specific requirements'
        }
    ]
    
    return jsonify({'jurisdictions': jurisdictions}), 200

@legal_bp.route('/compliance-info', methods=['GET'])
def get_compliance_info():
    """Get compliance information (legacy endpoint)"""
    compliance_info = {
        'gdpr': {
            'title': 'GDPR Compliance',
            'description': 'Information about GDPR compliance for EU users',
            'points': [
                'Right to access personal data',
                'Right to rectification of inaccurate data',
                'Right to erasure (right to be forgotten)',
                'Right to data portability',
                'Right to object to processing'
            ]
        },
        'ccpa': {
            'title': 'CCPA Compliance',
            'description': 'Information about CCPA compliance for California residents',
            'points': [
                'Right to know what personal information is collected',
                'Right to delete personal information',
                'Right to opt-out of sale of personal information',
                'Right to non-discrimination for exercising privacy rights'
            ]
        },
        'rufadaa': {
            'title': 'RUFADAA Compliance',
            'description': 'Revised Uniform Fiduciary Access to Digital Assets Act',
            'points': [
                'Provides legal framework for fiduciary access to digital assets',
                'Allows executors to manage digital assets with proper authorization',
                'Balances privacy rights with estate administration needs',
                'Enacted in most U.S. states with some variations'
            ]
        }
    }
    
    return jsonify({'compliance': compliance_info}), 200

