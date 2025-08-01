from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt
import secrets

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=True)  # Nullable for SSO users
    
    # Personal Information
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    address = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    zip_code = db.Column(db.String(20), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    
    # Executor Information
    executor_name = db.Column(db.String(200), nullable=True)
    executor_email = db.Column(db.String(255), nullable=True)
    digital_executor_name = db.Column(db.String(200), nullable=True)
    digital_executor_email = db.Column(db.String(255), nullable=True)
    
    # Security
    two_fa_enabled = db.Column(db.Boolean, default=False)
    two_fa_secret = db.Column(db.String(32), nullable=True)
    backup_codes = db.Column(db.Text, nullable=True)  # JSON array of backup codes
    
    # Account Status
    email_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    
    # SSO Information
    google_id = db.Column(db.String(100), nullable=True, unique=True)
    apple_id = db.Column(db.String(100), nullable=True, unique=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    sessions = db.relationship('UserSession', backref='user', lazy=True, cascade='all, delete-orphan')
    payments = db.relationship('Payment', backref='user', lazy=True)
    addendums = db.relationship('Addendum', backref='user', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        """Check if provided password matches hash"""
        if not self.password_hash:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def generate_backup_codes(self):
        """Generate backup codes for 2FA"""
        codes = [secrets.token_hex(4).upper() for _ in range(10)]
        self.backup_codes = ','.join(codes)
        return codes

    def verify_backup_code(self, code):
        """Verify and consume a backup code"""
        if not self.backup_codes:
            return False
        
        codes = self.backup_codes.split(',')
        if code.upper() in codes:
            codes.remove(code.upper())
            self.backup_codes = ','.join(codes)
            db.session.commit()
            return True
        return False

    def to_dict(self, include_sensitive=False):
        data = {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'executor_name': self.executor_name,
            'executor_email': self.executor_email,
            'digital_executor_name': self.digital_executor_name,
            'digital_executor_email': self.digital_executor_email,
            'two_fa_enabled': self.two_fa_enabled,
            'email_verified': self.email_verified,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
        
        if include_sensitive:
            data.update({
                'backup_codes': self.backup_codes.split(',') if self.backup_codes else [],
                'two_fa_secret': self.two_fa_secret
            })
        
        return data

class UserSession(db.Model):
    __tablename__ = 'user_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_token = db.Column(db.String(255), unique=True, nullable=False, index=True)
    refresh_token = db.Column(db.String(255), unique=True, nullable=True)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used = db.Column(db.DateTime, default=datetime.utcnow)
    user_agent = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<UserSession {self.session_token[:8]}...>'

    def is_expired(self):
        return datetime.utcnow() > self.expires_at

    def to_dict(self):
        return {
            'id': self.id,
            'session_token': self.session_token,
            'expires_at': self.expires_at.isoformat(),
            'created_at': self.created_at.isoformat(),
            'last_used': self.last_used.isoformat(),
            'user_agent': self.user_agent,
            'ip_address': self.ip_address,
            'is_active': self.is_active
        }
