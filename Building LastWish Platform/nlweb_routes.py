"""
Flask routes for NLWeb AI Integration in LastWish Estate Planning Platform
Provides AI-powered estate planning assistance and document generation
"""
from flask import Blueprint, request, jsonify, session
from models.user import db, User
from utils.nlweb_integration import NLWebEstateAssistant
import json

# Create blueprint
nlweb_bp = Blueprint('nlweb', __name__)

# Initialize NLWeb assistant
assistant = NLWebEstateAssistant()

@nlweb_bp.route('/analyze-estate', methods=['POST'])
def analyze_estate():
    """Analyze user's estate completeness and provide recommendations"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Not authenticated'}), 401
        
        data = request.get_json()
        estate_data = data.get('estate_data', {})
        
        # Get AI analysis
        analysis = assistant.analyze_estate_completeness(estate_data)
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@nlweb_bp.route('/generate-will', methods=['POST'])
def generate_will():
    """Generate will document using AI"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Not authenticated'}), 401
        
        data = request.get_json()
        will_data = data.get('will_data', {})
        
        # Generate will document
        will_document = assistant.generate_will_document(will_data)
        
        return jsonify({
            'success': True,
            'will_document': will_document
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@nlweb_bp.route('/chat', methods=['POST'])
def chat_consultation():
    """AI chat consultation for estate planning"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Not authenticated'}), 401
        
        data = request.get_json()
        message = data.get('message', '')
        context = data.get('context', {})
        
        # Get AI response
        response = assistant.chat_consultation(message, context)
        
        return jsonify({
            'success': True,
            'response': response
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@nlweb_bp.route('/recommendations', methods=['POST'])
def get_recommendations():
    """Get personalized estate planning recommendations"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Not authenticated'}), 401
        
        data = request.get_json()
        user_profile = data.get('user_profile', {})
        estate_data = data.get('estate_data', {})
        
        # Get AI recommendations
        recommendations = assistant.get_personalized_recommendations(user_profile, estate_data)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@nlweb_bp.route('/legal-compliance', methods=['POST'])
def check_legal_compliance():
    """Check legal compliance for estate planning documents"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Not authenticated'}), 401
        
        data = request.get_json()
        document_data = data.get('document_data', {})
        jurisdiction = data.get('jurisdiction', 'US')
        
        # Check legal compliance
        compliance_check = assistant.check_legal_compliance(document_data, jurisdiction)
        
        return jsonify({
            'success': True,
            'compliance_check': compliance_check
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

