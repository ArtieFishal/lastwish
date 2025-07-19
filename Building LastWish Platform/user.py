from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Authentication
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Personal Information
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    date_of_birth = db.Column(db.Date)
    phone = db.Column(db.String(20))
    
    # Address Information
    address_line_1 = db.Column(db.String(200))
    address_line_2 = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.String(20))
    country = db.Column(db.String(100), default='United States')
    
    # Legal Information
    ssn_last_four = db.Column(db.String(4))
    marital_status = db.Column(db.String(20))  # single, married, divorced, widowed
    
    # Account Status
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    email_verified = db.Column(db.Boolean, default=False)
    phone_verified = db.Column(db.Boolean, default=False)
    
    # Security
    two_factor_enabled = db.Column(db.Boolean, default=False)
    two_factor_secret = db.Column(db.String(32))
    last_login = db.Column(db.DateTime)
    failed_login_attempts = db.Column(db.Integer, default=0)
    account_locked_until = db.Column(db.DateTime)
    
    # Subscription and Billing
    subscription_tier = db.Column(db.String(20), default='free')  # free, basic, premium
    subscription_expires = db.Column(db.DateTime)
    
    # Preferences
    timezone = db.Column(db.String(50), default='UTC')
    notification_preferences = db.Column(db.Text)  # JSON string
    privacy_settings = db.Column(db.Text)  # JSON string
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    @property
    def full_name(self):
        """Get full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    @property
    def full_address(self):
        """Get formatted full address"""
        parts = []
        if self.address_line_1:
            parts.append(self.address_line_1)
        if self.address_line_2:
            parts.append(self.address_line_2)
        if self.city and self.state:
            parts.append(f"{self.city}, {self.state}")
        if self.zip_code:
            parts.append(self.zip_code)
        return '\n'.join(parts) if parts else None

    def to_dict(self, include_sensitive=False):
        """Convert to dictionary, optionally including sensitive data"""
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'phone': self.phone,
            'address_line_1': self.address_line_1,
            'address_line_2': self.address_line_2,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'country': self.country,
            'marital_status': self.marital_status,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'email_verified': self.email_verified,
            'phone_verified': self.phone_verified,
            'subscription_tier': self.subscription_tier,
            'subscription_expires': self.subscription_expires.isoformat() if self.subscription_expires else None,
            'timezone': self.timezone,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_sensitive:
            data.update({
                'ssn_last_four': self.ssn_last_four,
                'two_factor_enabled': self.two_factor_enabled,
                'last_login': self.last_login.isoformat() if self.last_login else None,
                'failed_login_attempts': self.failed_login_attempts,
                'notification_preferences': self.notification_preferences,
                'privacy_settings': self.privacy_settings
            })
        
        return data


# Import crypto models for relationships
from sqlalchemy.orm import relationship

# Add these relationships to the User class (add after the to_dict method)
"""
Crypto Asset Relationships - Add these to the User class:

crypto_wallets = relationship("CryptoWallet", back_populates="user", cascade="all, delete-orphan")
crypto_assets = relationship("CryptoAsset", back_populates="user", cascade="all, delete-orphan")
crypto_transactions = relationship("CryptoTransaction", back_populates="user", cascade="all, delete-orphan")
crypto_inheritance_plans = relationship("CryptoInheritancePlan", back_populates="user", cascade="all, delete-orphan")
crypto_beneficiaries = relationship("CryptoBeneficiary", back_populates="user", cascade="all, delete-orphan")
crypto_compliance_records = relationship("CryptoComplianceRecord", back_populates="user", cascade="all, delete-orphan")
"""

