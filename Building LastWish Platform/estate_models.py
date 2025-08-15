"""
LastWish Web3 Estate Planning Database Models
Comprehensive models for decentralized estate planning with crypto assets
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from decimal import Decimal

db = SQLAlchemy()

class User(db.Model):
    """User model for Web3 estate planning"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    wallet_address = db.Column(db.String(42), unique=True, nullable=False)  # Ethereum address
    ens_domain = db.Column(db.String(255), unique=True, nullable=True)  # ENS domain like lastwish.eth
    email = db.Column(db.String(255), unique=True, nullable=True)
    full_name = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(100), default='United States')
    marital_status = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    
    # Subscription and monetization
    subscription_tier = db.Column(db.String(50), default='free')  # free, basic, premium, enterprise
    subscription_expires = db.Column(db.DateTime, nullable=True)
    total_paid = db.Column(db.Numeric(10, 2), default=0.00)
    
    # Web3 specific
    preferred_network = db.Column(db.String(50), default='ethereum')  # ethereum, polygon, bsc, avalanche
    ipfs_hash = db.Column(db.String(255), nullable=True)  # IPFS hash for decentralized storage
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    wills = db.relationship('Will', backref='user', lazy=True, cascade='all, delete-orphan')
    assets = db.relationship('Asset', backref='user', lazy=True, cascade='all, delete-orphan')
    crypto_assets = db.relationship('CryptoAsset', backref='user', lazy=True, cascade='all, delete-orphan')
    beneficiaries = db.relationship('Beneficiary', backref='user', lazy=True, cascade='all, delete-orphan')
    smart_contracts = db.relationship('SmartContract', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'wallet_address': self.wallet_address,
            'ens_domain': self.ens_domain,
            'full_name': self.full_name,
            'subscription_tier': self.subscription_tier,
            'preferred_network': self.preferred_network,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Will(db.Model):
    """Digital will with Web3 integration"""
    __tablename__ = 'wills'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Will content
    title = db.Column(db.String(255), default='Last Will and Testament')
    executor_name = db.Column(db.String(255), nullable=False)
    executor_address = db.Column(db.Text, nullable=False)
    executor_phone = db.Column(db.String(20), nullable=False)
    executor_email = db.Column(db.String(255), nullable=False)
    
    # Guardian information (for minors)
    guardian_name = db.Column(db.String(255), nullable=True)
    guardian_address = db.Column(db.Text, nullable=True)
    guardian_phone = db.Column(db.String(20), nullable=True)
    
    # Final wishes
    funeral_preferences = db.Column(db.Text, nullable=True)
    burial_cremation = db.Column(db.String(50), nullable=True)  # burial, cremation, other
    special_instructions = db.Column(db.Text, nullable=True)
    
    # Legal and compliance
    jurisdiction = db.Column(db.String(100), nullable=False)
    witness_required = db.Column(db.Boolean, default=True)
    notarization_required = db.Column(db.Boolean, default=False)
    
    # Web3 integration
    smart_contract_address = db.Column(db.String(42), nullable=True)
    ipfs_hash = db.Column(db.String(255), nullable=True)
    blockchain_network = db.Column(db.String(50), default='ethereum')
    
    # Status and versioning
    status = db.Column(db.String(50), default='draft')  # draft, active, executed, revoked
    version = db.Column(db.Integer, default=1)
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    executed_at = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'executor_name': self.executor_name,
            'status': self.status,
            'jurisdiction': self.jurisdiction,
            'smart_contract_address': self.smart_contract_address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Asset(db.Model):
    """Traditional assets (real estate, vehicles, bank accounts, etc.)"""
    __tablename__ = 'assets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    will_id = db.Column(db.Integer, db.ForeignKey('wills.id'), nullable=True)
    
    # Asset details
    asset_type = db.Column(db.String(50), nullable=False)  # real_estate, vehicle, bank_account, investment, business, personal_property
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    estimated_value = db.Column(db.Numeric(15, 2), nullable=False)
    
    # Location and identification
    location = db.Column(db.Text, nullable=True)
    account_number = db.Column(db.String(255), nullable=True)
    institution_name = db.Column(db.String(255), nullable=True)
    
    # Legal documents
    deed_title_number = db.Column(db.String(255), nullable=True)
    vin_serial_number = db.Column(db.String(255), nullable=True)
    
    # Beneficiary assignment
    primary_beneficiary_id = db.Column(db.Integer, db.ForeignKey('beneficiaries.id'), nullable=True)
    inheritance_percentage = db.Column(db.Numeric(5, 2), default=100.00)
    
    # Status
    status = db.Column(db.String(50), default='active')  # active, sold, transferred, disputed
    verification_status = db.Column(db.String(50), default='pending')  # pending, verified, disputed
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    primary_beneficiary = db.relationship('Beneficiary', foreign_keys=[primary_beneficiary_id])
    
    def to_dict(self):
        return {
            'id': self.id,
            'asset_type': self.asset_type,
            'name': self.name,
            'description': self.description,
            'estimated_value': float(self.estimated_value),
            'status': self.status,
            'verification_status': self.verification_status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class CryptoAsset(db.Model):
    """Cryptocurrency and digital assets"""
    __tablename__ = 'crypto_assets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    will_id = db.Column(db.Integer, db.ForeignKey('wills.id'), nullable=True)
    
    # Crypto asset details
    asset_type = db.Column(db.String(50), nullable=False)  # cryptocurrency, nft, defi_position, dao_token
    token_symbol = db.Column(db.String(20), nullable=False)  # ETH, BTC, USDC, etc.
    token_name = db.Column(db.String(255), nullable=False)
    contract_address = db.Column(db.String(42), nullable=True)  # For ERC-20 tokens
    
    # Wallet and network information
    wallet_address = db.Column(db.String(42), nullable=False)
    network = db.Column(db.String(50), nullable=False)  # ethereum, polygon, bsc, avalanche
    
    # Asset quantity and value
    quantity = db.Column(db.Numeric(30, 18), nullable=False)  # Support for 18 decimal places
    estimated_value_usd = db.Column(db.Numeric(15, 2), nullable=True)
    
    # NFT specific fields
    token_id = db.Column(db.String(255), nullable=True)  # For NFTs
    metadata_uri = db.Column(db.Text, nullable=True)
    collection_name = db.Column(db.String(255), nullable=True)
    
    # DeFi specific fields
    protocol_name = db.Column(db.String(255), nullable=True)  # Uniswap, Aave, Compound, etc.
    position_type = db.Column(db.String(50), nullable=True)  # liquidity_pool, lending, staking
    
    # Inheritance configuration
    primary_beneficiary_id = db.Column(db.Integer, db.ForeignKey('beneficiaries.id'), nullable=True)
    inheritance_percentage = db.Column(db.Numeric(5, 2), default=100.00)
    smart_contract_id = db.Column(db.Integer, db.ForeignKey('smart_contracts.id'), nullable=True)
    
    # Access and recovery
    private_key_encrypted = db.Column(db.Text, nullable=True)  # Encrypted private key
    seed_phrase_encrypted = db.Column(db.Text, nullable=True)  # Encrypted seed phrase
    recovery_method = db.Column(db.String(100), nullable=True)  # smart_contract, multisig, social_recovery
    
    # Status
    status = db.Column(db.String(50), default='active')  # active, transferred, locked, disputed
    verification_status = db.Column(db.String(50), default='pending')  # pending, verified, disputed
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_balance_check = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    primary_beneficiary = db.relationship('Beneficiary', foreign_keys=[primary_beneficiary_id])
    smart_contract = db.relationship('SmartContract', foreign_keys=[smart_contract_id])
    
    def to_dict(self):
        return {
            'id': self.id,
            'asset_type': self.asset_type,
            'token_symbol': self.token_symbol,
            'token_name': self.token_name,
            'wallet_address': self.wallet_address,
            'network': self.network,
            'quantity': float(self.quantity),
            'estimated_value_usd': float(self.estimated_value_usd) if self.estimated_value_usd else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Beneficiary(db.Model):
    """Beneficiaries for estate planning"""
    __tablename__ = 'beneficiaries'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Personal information
    full_name = db.Column(db.String(255), nullable=False)
    relationship = db.Column(db.String(100), nullable=False)  # spouse, child, parent, sibling, friend, charity
    date_of_birth = db.Column(db.Date, nullable=True)
    
    # Contact information
    email = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    
    # Web3 information
    wallet_address = db.Column(db.String(42), nullable=True)
    ens_domain = db.Column(db.String(255), nullable=True)
    preferred_network = db.Column(db.String(50), default='ethereum')
    
    # Legal status
    is_minor = db.Column(db.Boolean, default=False)
    guardian_name = db.Column(db.String(255), nullable=True)
    guardian_contact = db.Column(db.String(255), nullable=True)
    
    # Inheritance details
    inheritance_percentage = db.Column(db.Numeric(5, 2), nullable=True)
    contingent_beneficiary = db.Column(db.Boolean, default=False)
    
    # Status and verification
    status = db.Column(db.String(50), default='active')  # active, inactive, deceased, disputed
    verification_status = db.Column(db.String(50), default='pending')  # pending, verified, disputed
    notification_sent = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_contacted = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'relationship': self.relationship,
            'email': self.email,
            'wallet_address': self.wallet_address,
            'ens_domain': self.ens_domain,
            'is_minor': self.is_minor,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class SmartContract(db.Model):
    """Smart contracts for automated inheritance"""
    __tablename__ = 'smart_contracts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Contract details
    contract_address = db.Column(db.String(42), nullable=False)
    network = db.Column(db.String(50), nullable=False)
    contract_type = db.Column(db.String(100), nullable=False)  # inheritance, multisig, timelock, social_recovery
    
    # Contract configuration
    trigger_condition = db.Column(db.String(100), nullable=False)  # time_based, heartbeat, manual, social_consensus
    trigger_duration = db.Column(db.Integer, nullable=True)  # Days for time-based triggers
    heartbeat_frequency = db.Column(db.Integer, nullable=True)  # Days between required heartbeats
    
    # Beneficiary configuration
    beneficiary_addresses = db.Column(db.Text, nullable=False)  # JSON array of addresses
    distribution_percentages = db.Column(db.Text, nullable=False)  # JSON array of percentages
    
    # Security features
    multisig_threshold = db.Column(db.Integer, nullable=True)  # Required signatures for multisig
    guardian_addresses = db.Column(db.Text, nullable=True)  # JSON array of guardian addresses
    emergency_contact = db.Column(db.String(255), nullable=True)
    
    # Contract status
    status = db.Column(db.String(50), default='deployed')  # deployed, active, triggered, executed, revoked
    deployment_tx_hash = db.Column(db.String(66), nullable=True)
    execution_tx_hash = db.Column(db.String(66), nullable=True)
    
    # Gas and fees
    deployment_gas_used = db.Column(db.Integer, nullable=True)
    deployment_gas_price = db.Column(db.Numeric(20, 0), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deployed_at = db.Column(db.DateTime, nullable=True)
    last_heartbeat = db.Column(db.DateTime, nullable=True)
    triggered_at = db.Column(db.DateTime, nullable=True)
    executed_at = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'contract_address': self.contract_address,
            'network': self.network,
            'contract_type': self.contract_type,
            'trigger_condition': self.trigger_condition,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Transaction(db.Model):
    """Blockchain transactions for audit trail"""
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Transaction details
    tx_hash = db.Column(db.String(66), nullable=False, unique=True)
    network = db.Column(db.String(50), nullable=False)
    block_number = db.Column(db.Integer, nullable=True)
    
    # Transaction type and purpose
    transaction_type = db.Column(db.String(100), nullable=False)  # contract_deployment, asset_transfer, heartbeat, execution
    purpose = db.Column(db.String(255), nullable=False)
    
    # Addresses involved
    from_address = db.Column(db.String(42), nullable=False)
    to_address = db.Column(db.String(42), nullable=False)
    
    # Value and gas
    value = db.Column(db.Numeric(30, 18), default=0)
    gas_used = db.Column(db.Integer, nullable=True)
    gas_price = db.Column(db.Numeric(20, 0), nullable=True)
    
    # Status
    status = db.Column(db.String(50), default='pending')  # pending, confirmed, failed
    confirmations = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed_at = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'tx_hash': self.tx_hash,
            'network': self.network,
            'transaction_type': self.transaction_type,
            'purpose': self.purpose,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Subscription(db.Model):
    """Subscription and payment tracking for monetization"""
    __tablename__ = 'subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Subscription details
    tier = db.Column(db.String(50), nullable=False)  # free, basic, premium, enterprise
    price_usd = db.Column(db.Numeric(10, 2), nullable=False)
    billing_cycle = db.Column(db.String(50), nullable=False)  # monthly, yearly, lifetime
    
    # Payment information
    payment_method = db.Column(db.String(50), nullable=False)  # crypto, stripe, paypal
    payment_address = db.Column(db.String(42), nullable=True)  # For crypto payments
    payment_tx_hash = db.Column(db.String(66), nullable=True)
    
    # Subscription period
    starts_at = db.Column(db.DateTime, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=True)
    auto_renew = db.Column(db.Boolean, default=True)
    
    # Status
    status = db.Column(db.String(50), default='active')  # active, expired, cancelled, suspended
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'tier': self.tier,
            'price_usd': float(self.price_usd),
            'billing_cycle': self.billing_cycle,
            'status': self.status,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None
        }

