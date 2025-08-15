import hashlib
import secrets
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app
from cryptography.fernet import Fernet
import base64
import os

class SecurityManager:
    """Enhanced security manager for LastWish platform"""
    
    def __init__(self):
        self.secret_key = current_app.config.get('SECRET_KEY', 'default-secret-key')
        self.encryption_key = self._get_or_create_encryption_key()
        self.cipher_suite = Fernet(self.encryption_key)
    
    def _get_or_create_encryption_key(self):
        """Get or create encryption key for sensitive data"""
        key_file = os.path.join(os.path.dirname(__file__), '..', 'encryption.key')
        
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key
    
    def hash_password(self, password: str, salt: str = None) -> tuple:
        """Hash password with salt using PBKDF2"""
        if salt is None:
            salt = secrets.token_hex(32)
        
        # Use PBKDF2 with SHA256
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000  # 100,000 iterations
        )
        
        return base64.b64encode(password_hash).decode('utf-8'), salt
    
    def verify_password(self, password: str, hashed_password: str, salt: str) -> bool:
        """Verify password against hash"""
        new_hash, _ = self.hash_password(password, salt)
        return secrets.compare_digest(new_hash, hashed_password)
    
    def generate_jwt_token(self, user_id: int, expires_in_hours: int = 24) -> str:
        """Generate JWT token for user authentication"""
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(hours=expires_in_hours),
            'iat': datetime.utcnow(),
            'type': 'access_token'
        }
        
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def generate_refresh_token(self, user_id: int) -> str:
        """Generate refresh token for token renewal"""
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(days=30),
            'iat': datetime.utcnow(),
            'type': 'refresh_token'
        }
        
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_jwt_token(self, token: str) -> dict:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            raise Exception('Token has expired')
        except jwt.InvalidTokenError:
            raise Exception('Invalid token')
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive data like SSN, account numbers"""
        if not data:
            return data
        
        encrypted_data = self.cipher_suite.encrypt(data.encode('utf-8'))
        return base64.b64encode(encrypted_data).decode('utf-8')
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        if not encrypted_data:
            return encrypted_data
        
        try:
            decoded_data = base64.b64decode(encrypted_data.encode('utf-8'))
            decrypted_data = self.cipher_suite.decrypt(decoded_data)
            return decrypted_data.decode('utf-8')
        except Exception:
            return encrypted_data  # Return as-is if decryption fails
    
    def generate_secure_token(self, length: int = 32) -> str:
        """Generate secure random token"""
        return secrets.token_urlsafe(length)
    
    def validate_password_strength(self, password: str) -> dict:
        """Validate password strength"""
        issues = []
        score = 0
        
        if len(password) < 8:
            issues.append("Password must be at least 8 characters long")
        else:
            score += 1
        
        if not any(c.isupper() for c in password):
            issues.append("Password must contain at least one uppercase letter")
        else:
            score += 1
        
        if not any(c.islower() for c in password):
            issues.append("Password must contain at least one lowercase letter")
        else:
            score += 1
        
        if not any(c.isdigit() for c in password):
            issues.append("Password must contain at least one number")
        else:
            score += 1
        
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            issues.append("Password must contain at least one special character")
        else:
            score += 1
        
        strength_levels = {
            0: "Very Weak",
            1: "Weak", 
            2: "Fair",
            3: "Good",
            4: "Strong",
            5: "Very Strong"
        }
        
        return {
            'is_valid': len(issues) == 0,
            'score': score,
            'strength': strength_levels[score],
            'issues': issues
        }

def require_auth(f):
    """Decorator to require authentication for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Check for token in Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid authorization header format'}), 401
        
        if not token:
            return jsonify({'error': 'Authentication token is missing'}), 401
        
        try:
            security_manager = SecurityManager()
            payload = security_manager.verify_jwt_token(token)
            
            # Add user_id to request context
            request.current_user_id = payload['user_id']
            
        except Exception as e:
            return jsonify({'error': str(e)}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function

def require_admin(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # First check authentication
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'error': 'Invalid authorization header format'}), 401
        
        if not token:
            return jsonify({'error': 'Authentication token is missing'}), 401
        
        try:
            security_manager = SecurityManager()
            payload = security_manager.verify_jwt_token(token)
            
            # Check if user is admin (you'll need to implement this in your User model)
            from src.models.user import User
            user = User.query.get(payload['user_id'])
            
            if not user or not getattr(user, 'is_admin', False):
                return jsonify({'error': 'Admin privileges required'}), 403
            
            request.current_user_id = payload['user_id']
            
        except Exception as e:
            return jsonify({'error': str(e)}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function

def rate_limit(max_requests: int = 100, window_minutes: int = 60):
    """Simple rate limiting decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Simple in-memory rate limiting (use Redis in production)
            client_ip = request.remote_addr
            
            # For now, just log the request (implement proper rate limiting in production)
            current_app.logger.info(f"Rate limit check for {client_ip}: {max_requests} requests per {window_minutes} minutes")
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def sanitize_input(data: dict, allowed_fields: list = None) -> dict:
    """Sanitize input data to prevent injection attacks"""
    if allowed_fields is None:
        return data
    
    sanitized = {}
    for field in allowed_fields:
        if field in data:
            value = data[field]
            if isinstance(value, str):
                # Basic XSS prevention
                value = value.replace('<', '&lt;').replace('>', '&gt;')
                value = value.replace('"', '&quot;').replace("'", '&#x27;')
            sanitized[field] = value
    
    return sanitized

def audit_log(action: str, user_id: int = None, details: dict = None):
    """Log security-relevant actions for audit trail"""
    log_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'action': action,
        'user_id': user_id,
        'ip_address': request.remote_addr if request else None,
        'user_agent': request.headers.get('User-Agent') if request else None,
        'details': details or {}
    }
    
    # Log to file (implement database logging in production)
    current_app.logger.info(f"AUDIT: {log_entry}")
    
    return log_entry

