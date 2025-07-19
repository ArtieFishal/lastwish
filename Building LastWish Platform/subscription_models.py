"""
Subscription and Payment Models for LastWish Estate Planning Platform
Handles monetization, subscription tiers, and payment processing
"""

from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from .estate_models import db

class SubscriptionTier(db.Model):
    """
    Subscription tier definitions with features and limits
    """
    __tablename__ = 'subscription_tiers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)  # Free, Basic, Premium, Enterprise
    display_name = Column(String(100), nullable=False)
    description = Column(Text)
    price_monthly = Column(Float, default=0.0)
    price_yearly = Column(Float, default=0.0)
    
    # Feature limits
    max_wills = Column(Integer, default=1)
    max_assets = Column(Integer, default=5)
    max_crypto_assets = Column(Integer, default=3)
    max_beneficiaries = Column(Integer, default=3)
    max_smart_contracts = Column(Integer, default=0)
    
    # Feature flags
    ai_assistance = Column(Boolean, default=False)
    priority_support = Column(Boolean, default=False)
    legal_review = Column(Boolean, default=False)
    document_generation = Column(Boolean, default=False)
    crypto_inheritance = Column(Boolean, default=False)
    smart_contract_deployment = Column(Boolean, default=False)
    custom_branding = Column(Boolean, default=False)
    api_access = Column(Boolean, default=False)
    
    # Metadata
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    subscriptions = relationship('UserSubscription', back_populates='tier')
    
    def __repr__(self):
        return f'<SubscriptionTier {self.name}: ${self.price_monthly}/month>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'price_monthly': self.price_monthly,
            'price_yearly': self.price_yearly,
            'features': {
                'max_wills': self.max_wills,
                'max_assets': self.max_assets,
                'max_crypto_assets': self.max_crypto_assets,
                'max_beneficiaries': self.max_beneficiaries,
                'max_smart_contracts': self.max_smart_contracts,
                'ai_assistance': self.ai_assistance,
                'priority_support': self.priority_support,
                'legal_review': self.legal_review,
                'document_generation': self.document_generation,
                'crypto_inheritance': self.crypto_inheritance,
                'smart_contract_deployment': self.smart_contract_deployment,
                'custom_branding': self.custom_branding,
                'api_access': self.api_access
            },
            'is_active': self.is_active,
            'sort_order': self.sort_order
        }

class UserSubscription(db.Model):
    """
    User subscription records with billing and status tracking
    """
    __tablename__ = 'user_subscriptions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    tier_id = Column(Integer, ForeignKey('subscription_tiers.id'), nullable=False)
    
    # Subscription details
    status = Column(String(20), default='active')  # active, cancelled, expired, suspended
    billing_cycle = Column(String(10), default='monthly')  # monthly, yearly
    start_date = Column(DateTime, default=datetime.now)
    end_date = Column(DateTime)
    next_billing_date = Column(DateTime)
    
    # Payment details
    amount_paid = Column(Float, default=0.0)
    currency = Column(String(3), default='USD')
    payment_method = Column(String(50))  # stripe, crypto, paypal
    stripe_subscription_id = Column(String(100))
    stripe_customer_id = Column(String(100))
    
    # Usage tracking
    wills_used = Column(Integer, default=0)
    assets_used = Column(Integer, default=0)
    crypto_assets_used = Column(Integer, default=0)
    beneficiaries_used = Column(Integer, default=0)
    smart_contracts_used = Column(Integer, default=0)
    ai_queries_used = Column(Integer, default=0)
    
    # Metadata
    auto_renew = Column(Boolean, default=True)
    cancelled_at = Column(DateTime)
    cancellation_reason = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    user = relationship('User', back_populates='subscription')
    tier = relationship('SubscriptionTier', back_populates='subscriptions')
    payments = relationship('Payment', back_populates='subscription')
    
    def __repr__(self):
        return f'<UserSubscription {self.user_id}: {self.tier.name} - {self.status}>'
    
    def is_active(self):
        """Check if subscription is currently active"""
        return (
            self.status == 'active' and 
            (self.end_date is None or self.end_date > datetime.now())
        )
    
    def is_expired(self):
        """Check if subscription has expired"""
        return self.end_date and self.end_date <= datetime.now()
    
    def days_remaining(self):
        """Get days remaining in subscription"""
        if self.end_date:
            delta = self.end_date - datetime.now()
            return max(0, delta.days)
        return None
    
    def usage_percentage(self, feature):
        """Get usage percentage for a specific feature"""
        used = getattr(self, f'{feature}_used', 0)
        limit = getattr(self.tier, f'max_{feature}', 0)
        
        if limit == 0:  # Unlimited
            return 0
        
        return min(100, (used / limit) * 100)
    
    def can_use_feature(self, feature, count=1):
        """Check if user can use a feature based on subscription limits"""
        if not self.is_active():
            return False
        
        used = getattr(self, f'{feature}_used', 0)
        limit = getattr(self.tier, f'max_{feature}', 0)
        
        # Unlimited usage
        if limit == 0:
            return True
        
        return (used + count) <= limit
    
    def increment_usage(self, feature, count=1):
        """Increment usage counter for a feature"""
        current_usage = getattr(self, f'{feature}_used', 0)
        setattr(self, f'{feature}_used', current_usage + count)
        self.updated_at = datetime.now()
        db.session.commit()
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'tier': self.tier.to_dict() if self.tier else None,
            'status': self.status,
            'billing_cycle': self.billing_cycle,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'next_billing_date': self.next_billing_date.isoformat() if self.next_billing_date else None,
            'amount_paid': self.amount_paid,
            'currency': self.currency,
            'payment_method': self.payment_method,
            'usage': {
                'wills_used': self.wills_used,
                'assets_used': self.assets_used,
                'crypto_assets_used': self.crypto_assets_used,
                'beneficiaries_used': self.beneficiaries_used,
                'smart_contracts_used': self.smart_contracts_used,
                'ai_queries_used': self.ai_queries_used
            },
            'auto_renew': self.auto_renew,
            'is_active': self.is_active(),
            'days_remaining': self.days_remaining()
        }

class Payment(db.Model):
    """
    Payment transaction records for subscription billing
    """
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True)
    subscription_id = Column(Integer, ForeignKey('user_subscriptions.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Payment details
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default='USD')
    payment_method = Column(String(50), nullable=False)  # stripe, crypto, paypal
    status = Column(String(20), default='pending')  # pending, completed, failed, refunded
    
    # External payment IDs
    stripe_payment_intent_id = Column(String(100))
    stripe_charge_id = Column(String(100))
    crypto_transaction_hash = Column(String(100))
    paypal_transaction_id = Column(String(100))
    
    # Crypto payment details
    crypto_currency = Column(String(10))  # ETH, BTC, USDC, etc.
    crypto_amount = Column(Float)
    crypto_wallet_address = Column(String(100))
    crypto_network = Column(String(20))  # ethereum, polygon, bsc
    
    # Billing details
    billing_period_start = Column(DateTime)
    billing_period_end = Column(DateTime)
    invoice_number = Column(String(50))
    
    # Metadata
    description = Column(Text)
    failure_reason = Column(Text)
    refund_amount = Column(Float, default=0.0)
    refunded_at = Column(DateTime)
    processed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    subscription = relationship('UserSubscription', back_populates='payments')
    user = relationship('User')
    
    def __repr__(self):
        return f'<Payment {self.id}: ${self.amount} - {self.status}>'
    
    def is_successful(self):
        """Check if payment was successful"""
        return self.status == 'completed'
    
    def is_pending(self):
        """Check if payment is pending"""
        return self.status == 'pending'
    
    def is_failed(self):
        """Check if payment failed"""
        return self.status == 'failed'
    
    def to_dict(self):
        return {
            'id': self.id,
            'subscription_id': self.subscription_id,
            'user_id': self.user_id,
            'amount': self.amount,
            'currency': self.currency,
            'payment_method': self.payment_method,
            'status': self.status,
            'crypto_details': {
                'currency': self.crypto_currency,
                'amount': self.crypto_amount,
                'wallet_address': self.crypto_wallet_address,
                'network': self.crypto_network,
                'transaction_hash': self.crypto_transaction_hash
            } if self.crypto_currency else None,
            'billing_period': {
                'start': self.billing_period_start.isoformat() if self.billing_period_start else None,
                'end': self.billing_period_end.isoformat() if self.billing_period_end else None
            },
            'invoice_number': self.invoice_number,
            'description': self.description,
            'processed_at': self.processed_at.isoformat() if self.processed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class PromoCode(db.Model):
    """
    Promotional codes for discounts and special offers
    """
    __tablename__ = 'promo_codes'
    
    id = Column(Integer, primary_key=True)
    code = Column(String(50), nullable=False, unique=True)
    description = Column(Text)
    
    # Discount details
    discount_type = Column(String(20), default='percentage')  # percentage, fixed_amount
    discount_value = Column(Float, nullable=False)  # 20 for 20% or 10.00 for $10
    max_discount_amount = Column(Float)  # Maximum discount for percentage types
    
    # Usage limits
    max_uses = Column(Integer)  # Maximum total uses
    max_uses_per_user = Column(Integer, default=1)
    current_uses = Column(Integer, default=0)
    
    # Validity period
    valid_from = Column(DateTime, default=datetime.now)
    valid_until = Column(DateTime)
    
    # Applicable tiers
    applicable_tiers = Column(String(200))  # Comma-separated tier IDs
    
    # Metadata
    is_active = Column(Boolean, default=True)
    created_by = Column(String(100))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f'<PromoCode {self.code}: {self.discount_value}{"%" if self.discount_type == "percentage" else " USD"}>'
    
    def is_valid(self):
        """Check if promo code is currently valid"""
        now = datetime.now()
        return (
            self.is_active and
            (self.valid_from is None or self.valid_from <= now) and
            (self.valid_until is None or self.valid_until >= now) and
            (self.max_uses is None or self.current_uses < self.max_uses)
        )
    
    def calculate_discount(self, amount):
        """Calculate discount amount for given price"""
        if not self.is_valid():
            return 0.0
        
        if self.discount_type == 'percentage':
            discount = amount * (self.discount_value / 100)
            if self.max_discount_amount:
                discount = min(discount, self.max_discount_amount)
            return discount
        elif self.discount_type == 'fixed_amount':
            return min(self.discount_value, amount)
        
        return 0.0
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'description': self.description,
            'discount_type': self.discount_type,
            'discount_value': self.discount_value,
            'max_discount_amount': self.max_discount_amount,
            'max_uses': self.max_uses,
            'max_uses_per_user': self.max_uses_per_user,
            'current_uses': self.current_uses,
            'valid_from': self.valid_from.isoformat() if self.valid_from else None,
            'valid_until': self.valid_until.isoformat() if self.valid_until else None,
            'applicable_tiers': self.applicable_tiers,
            'is_active': self.is_active,
            'is_valid': self.is_valid()
        }

class UsageLog(db.Model):
    """
    Detailed usage logging for analytics and billing
    """
    __tablename__ = 'usage_logs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    subscription_id = Column(Integer, ForeignKey('user_subscriptions.id'))
    
    # Usage details
    feature = Column(String(50), nullable=False)  # will_creation, asset_management, ai_query
    action = Column(String(50), nullable=False)  # create, update, delete, query
    resource_id = Column(String(100))  # ID of the resource being used
    
    # Metadata
    ip_address = Column(String(45))
    user_agent = Column(Text)
    session_id = Column(String(100))
    timestamp = Column(DateTime, default=datetime.now)
    
    # Additional data
    extra_data = Column(Text)  # JSON string for additional context
    
    def __repr__(self):
        return f'<UsageLog {self.user_id}: {self.feature}.{self.action}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'subscription_id': self.subscription_id,
            'feature': self.feature,
            'action': self.action,
            'resource_id': self.resource_id,
            'ip_address': self.ip_address,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'extra_data': self.extra_data
        }

# Utility functions for subscription management
def create_default_subscription_tiers():
    """Create default subscription tiers if they don't exist"""
    
    # Check if tiers already exist
    if SubscriptionTier.query.count() > 0:
        return
    
    # Free tier
    free_tier = SubscriptionTier(
        name='free',
        display_name='Free',
        description='Basic estate planning features for getting started',
        price_monthly=0.0,
        price_yearly=0.0,
        max_wills=1,
        max_assets=5,
        max_crypto_assets=3,
        max_beneficiaries=3,
        max_smart_contracts=0,
        ai_assistance=False,
        priority_support=False,
        legal_review=False,
        document_generation=True,
        crypto_inheritance=False,
        smart_contract_deployment=False,
        custom_branding=False,
        api_access=False,
        sort_order=1
    )
    
    # Basic tier
    basic_tier = SubscriptionTier(
        name='basic',
        display_name='Basic',
        description='Enhanced estate planning with AI assistance and crypto support',
        price_monthly=19.99,
        price_yearly=199.99,
        max_wills=3,
        max_assets=25,
        max_crypto_assets=15,
        max_beneficiaries=10,
        max_smart_contracts=2,
        ai_assistance=True,
        priority_support=False,
        legal_review=False,
        document_generation=True,
        crypto_inheritance=True,
        smart_contract_deployment=True,
        custom_branding=False,
        api_access=False,
        sort_order=2
    )
    
    # Premium tier
    premium_tier = SubscriptionTier(
        name='premium',
        display_name='Premium',
        description='Professional estate planning with legal review and priority support',
        price_monthly=49.99,
        price_yearly=499.99,
        max_wills=10,
        max_assets=100,
        max_crypto_assets=50,
        max_beneficiaries=25,
        max_smart_contracts=10,
        ai_assistance=True,
        priority_support=True,
        legal_review=True,
        document_generation=True,
        crypto_inheritance=True,
        smart_contract_deployment=True,
        custom_branding=True,
        api_access=False,
        sort_order=3
    )
    
    # Enterprise tier
    enterprise_tier = SubscriptionTier(
        name='enterprise',
        display_name='Enterprise',
        description='Unlimited estate planning for organizations and high-net-worth individuals',
        price_monthly=199.99,
        price_yearly=1999.99,
        max_wills=0,  # Unlimited
        max_assets=0,  # Unlimited
        max_crypto_assets=0,  # Unlimited
        max_beneficiaries=0,  # Unlimited
        max_smart_contracts=0,  # Unlimited
        ai_assistance=True,
        priority_support=True,
        legal_review=True,
        document_generation=True,
        crypto_inheritance=True,
        smart_contract_deployment=True,
        custom_branding=True,
        api_access=True,
        sort_order=4
    )
    
    # Add all tiers to database
    db.session.add_all([free_tier, basic_tier, premium_tier, enterprise_tier])
    db.session.commit()
    
    print("Default subscription tiers created successfully!")

def get_user_subscription(user_id):
    """Get active subscription for a user"""
    return UserSubscription.query.filter_by(
        user_id=user_id,
        status='active'
    ).first()

def check_feature_limit(user_id, feature, count=1):
    """Check if user can use a feature based on subscription limits"""
    subscription = get_user_subscription(user_id)
    
    if not subscription:
        # No subscription - use free tier limits
        free_tier = SubscriptionTier.query.filter_by(name='free').first()
        if not free_tier:
            return False
        
        # Create temporary subscription object for limit checking
        temp_subscription = UserSubscription(tier=free_tier)
        return temp_subscription.can_use_feature(feature, count)
    
    return subscription.can_use_feature(feature, count)

def log_feature_usage(user_id, feature, action, resource_id=None, metadata=None):
    """Log feature usage for analytics and billing"""
    subscription = get_user_subscription(user_id)
    
    usage_log = UsageLog(
        user_id=user_id,
        subscription_id=subscription.id if subscription else None,
        feature=feature,
        action=action,
        resource_id=resource_id,
        extra_data=metadata
    )
    
    db.session.add(usage_log)
    
    # Increment usage counter if it's a creation action
    if action == 'create' and subscription:
        subscription.increment_usage(feature)
    
    db.session.commit()

# Export all models and utility functions
__all__ = [
    'SubscriptionTier',
    'UserSubscription', 
    'Payment',
    'PromoCode',
    'UsageLog',
    'create_default_subscription_tiers',
    'get_user_subscription',
    'check_feature_limit',
    'log_feature_usage'
]

