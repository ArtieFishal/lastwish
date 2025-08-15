from flask import Blueprint, request, jsonify
from src.models.user import db, User
from src.models.estate import Will, Asset, Beneficiary, DigitalAsset
from datetime import datetime
import json
import logging

n8n_bp = Blueprint('n8n', __name__, url_prefix='/api/n8n')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@n8n_bp.route('/webhook/will-created', methods=['POST'])
def will_created_webhook():
    """
    Webhook endpoint for when a will is created
    Triggers document generation and notification workflows
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        will_id = data.get('will_id')
        
        if not user_id or not will_id:
            return jsonify({'error': 'Missing user_id or will_id'}), 400
        
        # Get user and will data
        user = User.query.get(user_id)
        will = Will.query.get(will_id)
        
        if not user or not will:
            return jsonify({'error': 'User or will not found'}), 404
        
        # Prepare data for n8n workflow
        workflow_data = {
            'user': {
                'id': user.id,
                'email': user.email,
                'name': f"{user.first_name} {user.last_name}",
                'phone': user.phone
            },
            'will': {
                'id': will.id,
                'title': will.title,
                'status': will.status,
                'created_at': will.created_at.isoformat(),
                'content': will.content
            },
            'trigger_type': 'will_created',
            'timestamp': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Will created webhook triggered for user {user_id}, will {will_id}")
        
        return jsonify({
            'status': 'success',
            'message': 'Will creation webhook processed',
            'data': workflow_data
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing will creation webhook: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@n8n_bp.route('/webhook/beneficiary-added', methods=['POST'])
def beneficiary_added_webhook():
    """
    Webhook endpoint for when a beneficiary is added
    Triggers notification and verification workflows
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        beneficiary_id = data.get('beneficiary_id')
        
        if not user_id or not beneficiary_id:
            return jsonify({'error': 'Missing user_id or beneficiary_id'}), 400
        
        # Get user and beneficiary data
        user = User.query.get(user_id)
        beneficiary = Beneficiary.query.get(beneficiary_id)
        
        if not user or not beneficiary:
            return jsonify({'error': 'User or beneficiary not found'}), 404
        
        # Prepare data for n8n workflow
        workflow_data = {
            'user': {
                'id': user.id,
                'email': user.email,
                'name': f"{user.first_name} {user.last_name}"
            },
            'beneficiary': {
                'id': beneficiary.id,
                'name': f"{beneficiary.first_name} {beneficiary.last_name}",
                'email': beneficiary.email,
                'phone': beneficiary.phone,
                'relationship': beneficiary.relationship,
                'is_minor': beneficiary.is_minor
            },
            'trigger_type': 'beneficiary_added',
            'timestamp': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Beneficiary added webhook triggered for user {user_id}, beneficiary {beneficiary_id}")
        
        return jsonify({
            'status': 'success',
            'message': 'Beneficiary addition webhook processed',
            'data': workflow_data
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing beneficiary addition webhook: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@n8n_bp.route('/webhook/asset-updated', methods=['POST'])
def asset_updated_webhook():
    """
    Webhook endpoint for when an asset is updated
    Triggers valuation and distribution workflows
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        asset_id = data.get('asset_id')
        
        if not user_id or not asset_id:
            return jsonify({'error': 'Missing user_id or asset_id'}), 400
        
        # Get user and asset data
        user = User.query.get(user_id)
        asset = Asset.query.get(asset_id)
        
        if not user or not asset:
            return jsonify({'error': 'User or asset not found'}), 404
        
        # Get asset distributions
        distributions = []
        for distribution in asset.distributions:
            distributions.append({
                'beneficiary_id': distribution.beneficiary_id,
                'percentage': float(distribution.percentage) if distribution.percentage else None,
                'specific_amount': float(distribution.specific_amount) if distribution.specific_amount else None
            })
        
        # Prepare data for n8n workflow
        workflow_data = {
            'user': {
                'id': user.id,
                'email': user.email,
                'name': f"{user.first_name} {user.last_name}"
            },
            'asset': {
                'id': asset.id,
                'name': asset.name,
                'type': asset.asset_type,
                'estimated_value': float(asset.estimated_value) if asset.estimated_value else 0,
                'description': asset.description,
                'distributions': distributions
            },
            'trigger_type': 'asset_updated',
            'timestamp': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Asset updated webhook triggered for user {user_id}, asset {asset_id}")
        
        return jsonify({
            'status': 'success',
            'message': 'Asset update webhook processed',
            'data': workflow_data
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing asset update webhook: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@n8n_bp.route('/api/generate-document', methods=['POST'])
def generate_document():
    """
    API endpoint for n8n to trigger document generation
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        document_type = data.get('document_type', 'will')
        
        if not user_id:
            return jsonify({'error': 'Missing user_id'}), 400
        
        # Get user data
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get user's estate planning data
        wills = Will.query.filter_by(user_id=user_id).all()
        assets = Asset.query.filter_by(user_id=user_id).all()
        beneficiaries = Beneficiary.query.filter_by(user_id=user_id).all()
        
        # Prepare document data
        document_data = {
            'user': {
                'id': user.id,
                'name': f"{user.first_name} {user.last_name}",
                'email': user.email,
                'address': user.address,
                'city': user.city,
                'state': user.state,
                'zip_code': user.zip_code
            },
            'wills': [{'id': w.id, 'title': w.title, 'content': w.content, 'status': w.status} for w in wills],
            'assets': [{
                'id': a.id,
                'name': a.name,
                'type': a.asset_type,
                'value': float(a.estimated_value) if a.estimated_value else 0,
                'description': a.description
            } for a in assets],
            'beneficiaries': [{
                'id': b.id,
                'name': f"{b.first_name} {b.last_name}",
                'relationship': b.relationship,
                'email': b.email,
                'is_minor': b.is_minor
            } for b in beneficiaries],
            'document_type': document_type,
            'generated_at': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Document generation requested for user {user_id}, type {document_type}")
        
        return jsonify({
            'status': 'success',
            'message': 'Document data prepared for generation',
            'data': document_data
        }), 200
        
    except Exception as e:
        logger.error(f"Error preparing document generation: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@n8n_bp.route('/api/send-notification', methods=['POST'])
def send_notification():
    """
    API endpoint for n8n to send notifications
    """
    try:
        data = request.get_json()
        notification_type = data.get('type')
        recipient_email = data.get('recipient_email')
        message = data.get('message')
        subject = data.get('subject')
        
        if not all([notification_type, recipient_email, message, subject]):
            return jsonify({'error': 'Missing required notification data'}), 400
        
        # Prepare notification data for n8n workflow
        notification_data = {
            'type': notification_type,
            'recipient': recipient_email,
            'subject': subject,
            'message': message,
            'sent_at': datetime.utcnow().isoformat(),
            'status': 'queued'
        }
        
        logger.info(f"Notification queued: {notification_type} to {recipient_email}")
        
        return jsonify({
            'status': 'success',
            'message': 'Notification queued for sending',
            'data': notification_data
        }), 200
        
    except Exception as e:
        logger.error(f"Error queuing notification: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@n8n_bp.route('/api/legal-compliance-check', methods=['POST'])
def legal_compliance_check():
    """
    API endpoint for n8n to perform legal compliance checks
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        state = data.get('state')
        
        if not user_id:
            return jsonify({'error': 'Missing user_id'}), 400
        
        # Get user's estate planning data
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        wills = Will.query.filter_by(user_id=user_id).all()
        assets = Asset.query.filter_by(user_id=user_id).all()
        beneficiaries = Beneficiary.query.filter_by(user_id=user_id).all()
        
        # Perform basic compliance checks
        compliance_issues = []
        
        # Check if user has a will
        if not wills:
            compliance_issues.append({
                'type': 'missing_will',
                'severity': 'high',
                'message': 'No will document found'
            })
        
        # Check if all assets have beneficiaries
        for asset in assets:
            if not asset.distributions:
                compliance_issues.append({
                    'type': 'unassigned_asset',
                    'severity': 'medium',
                    'message': f'Asset "{asset.name}" has no assigned beneficiaries',
                    'asset_id': asset.id
                })
        
        # Check for minor beneficiaries without guardians
        for beneficiary in beneficiaries:
            if beneficiary.is_minor and not beneficiary.guardian_info:
                compliance_issues.append({
                    'type': 'minor_without_guardian',
                    'severity': 'high',
                    'message': f'Minor beneficiary "{beneficiary.first_name} {beneficiary.last_name}" has no assigned guardian',
                    'beneficiary_id': beneficiary.id
                })
        
        compliance_data = {
            'user_id': user_id,
            'state': state or user.state,
            'check_date': datetime.utcnow().isoformat(),
            'issues_found': len(compliance_issues),
            'compliance_score': max(0, 100 - (len(compliance_issues) * 10)),
            'issues': compliance_issues,
            'recommendations': [
                'Ensure all assets have designated beneficiaries',
                'Assign guardians for all minor beneficiaries',
                'Review state-specific legal requirements',
                'Consider professional legal review'
            ]
        }
        
        logger.info(f"Legal compliance check completed for user {user_id}: {len(compliance_issues)} issues found")
        
        return jsonify({
            'status': 'success',
            'message': 'Legal compliance check completed',
            'data': compliance_data
        }), 200
        
    except Exception as e:
        logger.error(f"Error performing legal compliance check: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@n8n_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for n8n workflows
    """
    return jsonify({
        'status': 'healthy',
        'service': 'LastWish N8N Integration API',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

