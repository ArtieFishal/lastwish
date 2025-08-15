from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
from jose import jwt, JWTError
from functools import wraps
import secrets
import re

from src.models.user import User, UserSession, db
from src.models.notification import NotificationTemplate
from src.services.email_service import EmailService
from src.utils.validation import validate_email, validate_password, validate_sensitive_data

auth_bp = Blueprint('auth', __name__)

def generate_tokens(user_id):
    """Generate access and refresh tokens"""
    now = datetime.utcnow()
    
    # Access token (short-lived)
    access_payload = {
        'user_id': user_id,
        'type': 'access',
        'iat': now,
        'exp': now + timedelta(seconds=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'])
    }
    
    # Refresh token (long-lived)
    refresh_payload = {
        'user_id': user_id,
        'type': 'refresh',
        'iat': now,
        'exp': now + timedelta(days=30)
    }
    
    access_token = jwt.encode(access_payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
    refresh_token = jwt.encode(refresh_payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
    
    return access_token, refresh_token

def verify_token(token, token_type='access'):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        if payload.get('type') != token_type:
            return None
        return payload
    except JWTError:
        return None

def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid authorization header'}), 401
        
        token = auth_header.split(' ')[1]
        payload = verify_token(token)
        
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        user = User.query.get(payload['user_id'])
        if not user or not user.is_active:
            return jsonify({'error': 'User not found or inactive'}), 401
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        request.current_user = user
        return f(*args, **kwargs)
    
    return decorated_function

@auth_bp.route('/register', methods=['POST'])
def register():
    """User registration"""
    try:
        data = request.get_json()
        
        # Validate required fields
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        
        if not all([email, password, first_name, last_name]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Validate email format
        if not validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate password strength
        password_errors = validate_password(password)
        if password_errors:
            return jsonify({'error': 'Password validation failed', 'details': password_errors}), 400
        
        # Check for sensitive data in input
        sensitive_fields = ['first_name', 'last_name', 'address', 'city']
        for field in sensitive_fields:
            value = data.get(field, '')
            if validate_sensitive_data(value):
                return jsonify({
                    'error': f'Sensitive data detected in {field}. Never enter private keys, seed phrases, or passwords.'
                }), 400
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 409
        
        # Create new user
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            address=data.get('address', '').strip(),
            city=data.get('city', '').strip(),
            state=data.get('state', '').strip(),
            zip_code=data.get('zip_code', '').strip(),
            executor_name=data.get('executor_name', '').strip(),
            executor_email=data.get('executor_email', '').strip().lower(),
            digital_executor_name=data.get('digital_executor_name', '').strip(),
            digital_executor_email=data.get('digital_executor_email', '').strip().lower()
        )
        
        # Parse date of birth if provided
        if data.get('date_of_birth'):
            try:
                user.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Generate tokens
        access_token, refresh_token = generate_tokens(user.id)
        
        # Create session
        session = UserSession(
            user_id=user.id,
            session_token=access_token,
            refresh_token=refresh_token,
            expires_at=datetime.utcnow() + timedelta(seconds=current_app.config['JWT_ACCESS_TOKEN_EXPIRES']),
            user_agent=request.headers.get('User-Agent'),
            ip_address=request.remote_addr
        )
        
        db.session.add(session)
        db.session.commit()
        
        # Send welcome email
        try:
            email_service = EmailService()
            email_service.send_welcome_email(user)
        except Exception as e:
            current_app.logger.error(f"Failed to send welcome email: {str(e)}")
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Registration error: {str(e)}")
        return jsonify({'error': 'Registration failed'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login"""
    try:
        data = request.get_json()
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 401
        
        # Generate tokens
        access_token, refresh_token = generate_tokens(user.id)
        
        # Create session
        session = UserSession(
            user_id=user.id,
            session_token=access_token,
            refresh_token=refresh_token,
            expires_at=datetime.utcnow() + timedelta(seconds=current_app.config['JWT_ACCESS_TOKEN_EXPIRES']),
            user_agent=request.headers.get('User-Agent'),
            ip_address=request.remote_addr
        )
        
        db.session.add(session)
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Login failed'}), 500

@auth_bp.route('/refresh', methods=['POST'])
def refresh_token():
    """Refresh access token"""
    try:
        data = request.get_json()
        refresh_token = data.get('refresh_token')
        
        if not refresh_token:
            return jsonify({'error': 'Refresh token required'}), 400
        
        # Verify refresh token
        payload = verify_token(refresh_token, 'refresh')
        if not payload:
            return jsonify({'error': 'Invalid or expired refresh token'}), 401
        
        # Find user
        user = User.query.get(payload['user_id'])
        if not user or not user.is_active:
            return jsonify({'error': 'User not found or inactive'}), 401
        
        # Generate new tokens
        new_access_token, new_refresh_token = generate_tokens(user.id)
        
        # Update session
        session = UserSession.query.filter_by(refresh_token=refresh_token).first()
        if session:
            session.session_token = new_access_token
            session.refresh_token = new_refresh_token
            session.expires_at = datetime.utcnow() + timedelta(seconds=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'])
            session.last_used = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'access_token': new_access_token,
            'refresh_token': new_refresh_token
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Token refresh error: {str(e)}")
        return jsonify({'error': 'Token refresh failed'}), 500

@auth_bp.route('/logout', methods=['POST'])
@require_auth
def logout():
    """User logout"""
    try:
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(' ')[1]
        
        # Deactivate session
        session = UserSession.query.filter_by(session_token=token).first()
        if session:
            session.is_active = False
            db.session.commit()
        
        return jsonify({'message': 'Logged out successfully'}), 200
        
    except Exception as e:
        current_app.logger.error(f"Logout error: {str(e)}")
        return jsonify({'error': 'Logout failed'}), 500

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """Request password reset"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        
        if not email:
            return jsonify({'error': 'Email required'}), 400
        
        user = User.query.filter_by(email=email).first()
        
        # Always return success to prevent email enumeration
        if user and user.is_active:
            # Generate reset token
            reset_token = secrets.token_urlsafe(32)
            
            # Store reset token (in production, use Redis or database)
            # For now, we'll use a simple approach
            
            try:
                email_service = EmailService()
                email_service.send_password_reset_email(user, reset_token)
            except Exception as e:
                current_app.logger.error(f"Failed to send password reset email: {str(e)}")
        
        return jsonify({'message': 'If the email exists, a password reset link has been sent'}), 200
        
    except Exception as e:
        current_app.logger.error(f"Password reset error: {str(e)}")
        return jsonify({'error': 'Password reset request failed'}), 500

@auth_bp.route('/verify-email', methods=['POST'])
def verify_email():
    """Verify email address"""
    try:
        data = request.get_json()
        token = data.get('token')
        
        if not token:
            return jsonify({'error': 'Verification token required'}), 400
        
        # Verify token and update user
        # Implementation depends on how verification tokens are stored
        
        return jsonify({'message': 'Email verified successfully'}), 200
        
    except Exception as e:
        current_app.logger.error(f"Email verification error: {str(e)}")
        return jsonify({'error': 'Email verification failed'}), 500

@auth_bp.route('/me', methods=['GET'])
@require_auth
def get_current_user():
    """Get current user information"""
    try:
        user = request.current_user
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        current_app.logger.error(f"Get current user error: {str(e)}")
        return jsonify({'error': 'Failed to get user information'}), 500

@auth_bp.route('/sessions', methods=['GET'])
@require_auth
def get_user_sessions():
    """Get user's active sessions"""
    try:
        user = request.current_user
        sessions = UserSession.query.filter_by(user_id=user.id, is_active=True).all()
        
        return jsonify({
            'sessions': [session.to_dict() for session in sessions]
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Get sessions error: {str(e)}")
        return jsonify({'error': 'Failed to get sessions'}), 500

@auth_bp.route('/sessions/<int:session_id>', methods=['DELETE'])
@require_auth
def revoke_session(session_id):
    """Revoke a specific session"""
    try:
        user = request.current_user
        session = UserSession.query.filter_by(id=session_id, user_id=user.id).first()
        
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        session.is_active = False
        db.session.commit()
        
        return jsonify({'message': 'Session revoked successfully'}), 200
        
    except Exception as e:
        current_app.logger.error(f"Revoke session error: {str(e)}")
        return jsonify({'error': 'Failed to revoke session'}), 500

