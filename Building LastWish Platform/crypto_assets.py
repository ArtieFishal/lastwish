"""
Cryptocurrency and Blockchain Asset Models for LastWish Estate Planning Platform
Comprehensive data models for managing digital assets, wallets, and blockchain-based inheritance
"""

from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Numeric, JSON, Enum
from sqlalchemy.orm import relationship
from models.user import db
import enum

class WalletType(enum.Enum):
    """Enumeration of supported wallet types"""
    HARDWARE = "hardware"
    SOFTWARE = "software"
    CUSTODIAL = "custodial"
    MULTISIG = "multisig"
    SMART_CONTRACT = "smart_contract"
    DEFI_PROTOCOL = "defi_protocol"

class AssetType(enum.Enum):
    """Enumeration of supported crypto asset types"""
    CRYPTOCURRENCY = "cryptocurrency"
    NFT = "nft"
    TOKEN = "token"
    DEFI_POSITION = "defi_position"
    STAKING_REWARD = "staking_reward"
    LIQUIDITY_POOL = "liquidity_pool"
    GOVERNANCE_TOKEN = "governance_token"

class BlockchainNetwork(enum.Enum):
    """Enumeration of supported blockchain networks"""
    BITCOIN = "bitcoin"
    ETHEREUM = "ethereum"
    BINANCE_SMART_CHAIN = "binance_smart_chain"
    POLYGON = "polygon"
    AVALANCHE = "avalanche"
    SOLANA = "solana"
    CARDANO = "cardano"
    POLKADOT = "polkadot"
    ARBITRUM = "arbitrum"
    OPTIMISM = "optimism"

class InheritanceStatus(enum.Enum):
    """Enumeration of inheritance planning status"""
    NOT_PLANNED = "not_planned"
    IN_PROGRESS = "in_progress"
    CONFIGURED = "configured"
    ACTIVE = "active"
    EXECUTED = "executed"
    FAILED = "failed"

class CryptoWallet(db.Model):
    """Model for cryptocurrency wallets and accounts"""
    __tablename__ = 'crypto_wallets'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Wallet identification
    wallet_name = Column(String(255), nullable=False)
    wallet_type = Column(Enum(WalletType), nullable=False)
    blockchain_network = Column(Enum(BlockchainNetwork), nullable=False)
    wallet_address = Column(String(255), nullable=False)
    
    # Security and access
    encrypted_private_key = Column(Text)  # Encrypted storage
    public_key = Column(Text)
    seed_phrase_encrypted = Column(Text)  # Encrypted seed phrase
    access_method = Column(String(100))  # How to access (hardware device, software, etc.)
    
    # Custodial information
    custodial_service = Column(String(255))  # Exchange or service name
    account_identifier = Column(String(255))  # Account ID or username
    
    # Multi-signature configuration
    multisig_threshold = Column(Integer)  # Required signatures
    multisig_total = Column(Integer)  # Total possible signers
    multisig_participants = Column(JSON)  # List of participant addresses/info
    
    # Metadata
    wallet_description = Column(Text)
    estimated_total_value = Column(Numeric(20, 8), default=0)
    last_balance_update = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    # Inheritance configuration
    inheritance_status = Column(Enum(InheritanceStatus), default=InheritanceStatus.NOT_PLANNED)
    inheritance_instructions = Column(Text)
    backup_location = Column(String(500))  # Where backup info is stored
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="crypto_wallets")
    crypto_assets = relationship("CryptoAsset", back_populates="wallet", cascade="all, delete-orphan")
    inheritance_plans = relationship("CryptoInheritancePlan", back_populates="wallet")
    
    def __repr__(self):
        return f'<CryptoWallet {self.wallet_name} ({self.wallet_type.value})>'

class CryptoAsset(db.Model):
    """Model for individual cryptocurrency assets and tokens"""
    __tablename__ = 'crypto_assets'
    
    id = Column(Integer, primary_key=True)
    wallet_id = Column(Integer, ForeignKey('crypto_wallets.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Asset identification
    asset_name = Column(String(255), nullable=False)
    asset_symbol = Column(String(20), nullable=False)
    asset_type = Column(Enum(AssetType), nullable=False)
    contract_address = Column(String(255))  # For tokens and smart contracts
    token_id = Column(String(255))  # For NFTs
    
    # Quantity and valuation
    quantity = Column(Numeric(30, 18), nullable=False)  # High precision for crypto
    current_price_usd = Column(Numeric(20, 8))
    current_value_usd = Column(Numeric(20, 8))
    purchase_price_usd = Column(Numeric(20, 8))
    purchase_date = Column(DateTime)
    
    # Asset metadata
    asset_description = Column(Text)
    metadata_uri = Column(String(500))  # For NFTs and complex assets
    asset_metadata = Column(JSON)  # Additional asset-specific data
    
    # DeFi and staking information
    staking_protocol = Column(String(255))
    staking_rewards_rate = Column(Numeric(10, 6))  # Annual percentage
    liquidity_pool_info = Column(JSON)
    defi_protocol_data = Column(JSON)
    
    # Inheritance planning
    inheritance_percentage = Column(Numeric(5, 2), default=100.00)  # Percentage to inherit
    inheritance_conditions = Column(Text)
    inheritance_beneficiaries = Column(JSON)  # List of beneficiary allocations
    
    # Risk and compliance
    risk_level = Column(String(50), default='medium')
    compliance_status = Column(String(100), default='compliant')
    regulatory_notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_price_update = Column(DateTime)
    
    # Relationships
    wallet = relationship("CryptoWallet", back_populates="crypto_assets")
    user = relationship("User", back_populates="crypto_assets")
    transactions = relationship("CryptoTransaction", back_populates="asset")
    
    def __repr__(self):
        return f'<CryptoAsset {self.asset_symbol}: {self.quantity}>'

class CryptoTransaction(db.Model):
    """Model for cryptocurrency transaction history"""
    __tablename__ = 'crypto_transactions'
    
    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey('crypto_assets.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Transaction identification
    transaction_hash = Column(String(255), unique=True)
    block_number = Column(Integer)
    transaction_index = Column(Integer)
    
    # Transaction details
    transaction_type = Column(String(50), nullable=False)  # buy, sell, transfer, stake, etc.
    from_address = Column(String(255))
    to_address = Column(String(255))
    quantity = Column(Numeric(30, 18), nullable=False)
    price_per_unit = Column(Numeric(20, 8))
    total_value_usd = Column(Numeric(20, 8))
    
    # Fees and costs
    gas_fee = Column(Numeric(20, 8))
    transaction_fee = Column(Numeric(20, 8))
    exchange_fee = Column(Numeric(20, 8))
    
    # Metadata
    transaction_description = Column(Text)
    exchange_or_platform = Column(String(255))
    transaction_metadata = Column(JSON)
    
    # Timestamps
    transaction_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    asset = relationship("CryptoAsset", back_populates="transactions")
    user = relationship("User", back_populates="crypto_transactions")
    
    def __repr__(self):
        return f'<CryptoTransaction {self.transaction_type}: {self.quantity}>'

class CryptoInheritancePlan(db.Model):
    """Model for cryptocurrency inheritance planning and automation"""
    __tablename__ = 'crypto_inheritance_plans'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    wallet_id = Column(Integer, ForeignKey('crypto_wallets.id'), nullable=False)
    
    # Plan identification
    plan_name = Column(String(255), nullable=False)
    plan_description = Column(Text)
    plan_status = Column(Enum(InheritanceStatus), default=InheritanceStatus.NOT_PLANNED)
    
    # Beneficiary information
    beneficiaries = Column(JSON, nullable=False)  # List of beneficiaries with allocations
    backup_beneficiaries = Column(JSON)  # Contingent beneficiaries
    
    # Execution conditions
    trigger_conditions = Column(JSON)  # Conditions that trigger inheritance
    time_delay = Column(Integer)  # Days before execution
    verification_requirements = Column(JSON)  # Required verifications
    
    # Smart contract integration
    smart_contract_address = Column(String(255))
    smart_contract_network = Column(Enum(BlockchainNetwork))
    contract_deployment_hash = Column(String(255))
    
    # Automation settings
    automated_execution = Column(Boolean, default=False)
    manual_approval_required = Column(Boolean, default=True)
    multi_signature_required = Column(Boolean, default=False)
    
    # Security and access
    access_instructions = Column(Text)
    security_questions = Column(JSON)
    emergency_contacts = Column(JSON)
    legal_documentation = Column(Text)
    
    # Execution tracking
    execution_date = Column(DateTime)
    execution_status = Column(String(100))
    execution_transaction_hash = Column(String(255))
    execution_notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_verification = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="crypto_inheritance_plans")
    wallet = relationship("CryptoWallet", back_populates="inheritance_plans")
    
    def __repr__(self):
        return f'<CryptoInheritancePlan {self.plan_name}>'

class CryptoBeneficiary(db.Model):
    """Model for cryptocurrency inheritance beneficiaries"""
    __tablename__ = 'crypto_beneficiaries'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Beneficiary identification
    beneficiary_name = Column(String(255), nullable=False)
    relationship_to_user = Column(String(100))
    beneficiary_type = Column(String(50), default='individual')  # individual, organization, charity
    
    # Contact information
    email_address = Column(String(255))
    phone_number = Column(String(50))
    physical_address = Column(Text)
    
    # Crypto-specific information
    crypto_wallet_address = Column(String(255))
    preferred_blockchain = Column(Enum(BlockchainNetwork))
    crypto_experience_level = Column(String(50), default='beginner')
    
    # Legal and verification
    legal_name = Column(String(255))
    date_of_birth = Column(DateTime)
    government_id_type = Column(String(100))
    government_id_number = Column(String(255))  # Encrypted
    
    # Inheritance allocations
    default_allocation_percentage = Column(Numeric(5, 2), default=0.00)
    specific_asset_allocations = Column(JSON)  # Asset-specific allocations
    
    # Status and verification
    verification_status = Column(String(100), default='unverified')
    verification_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    # Special instructions
    inheritance_instructions = Column(Text)
    educational_resources_sent = Column(Boolean, default=False)
    support_contact_info = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="crypto_beneficiaries")
    
    def __repr__(self):
        return f'<CryptoBeneficiary {self.beneficiary_name}>'

class CryptoMarketData(db.Model):
    """Model for cryptocurrency market data and pricing"""
    __tablename__ = 'crypto_market_data'
    
    id = Column(Integer, primary_key=True)
    
    # Asset identification
    asset_symbol = Column(String(20), nullable=False)
    asset_name = Column(String(255))
    contract_address = Column(String(255))
    blockchain_network = Column(Enum(BlockchainNetwork))
    
    # Pricing data
    price_usd = Column(Numeric(20, 8), nullable=False)
    price_btc = Column(Numeric(20, 8))
    price_eth = Column(Numeric(20, 8))
    
    # Market metrics
    market_cap_usd = Column(Numeric(20, 2))
    volume_24h_usd = Column(Numeric(20, 2))
    circulating_supply = Column(Numeric(30, 8))
    total_supply = Column(Numeric(30, 8))
    
    # Price changes
    price_change_24h = Column(Numeric(10, 6))
    price_change_7d = Column(Numeric(10, 6))
    price_change_30d = Column(Numeric(10, 6))
    
    # Additional data
    all_time_high = Column(Numeric(20, 8))
    all_time_low = Column(Numeric(20, 8))
    market_rank = Column(Integer)
    
    # Data source and quality
    data_source = Column(String(100), nullable=False)
    data_quality_score = Column(Numeric(3, 2), default=1.00)
    last_updated = Column(DateTime, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<CryptoMarketData {self.asset_symbol}: ${self.price_usd}>'

class CryptoComplianceRecord(db.Model):
    """Model for cryptocurrency compliance and regulatory tracking"""
    __tablename__ = 'crypto_compliance_records'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Compliance event
    compliance_type = Column(String(100), nullable=False)  # tax_report, kyc_verification, etc.
    compliance_status = Column(String(50), nullable=False)
    compliance_description = Column(Text)
    
    # Regulatory information
    jurisdiction = Column(String(100))
    regulatory_framework = Column(String(255))
    compliance_requirements = Column(JSON)
    
    # Associated assets and transactions
    affected_assets = Column(JSON)  # List of asset IDs
    affected_transactions = Column(JSON)  # List of transaction IDs
    
    # Documentation
    supporting_documents = Column(JSON)  # List of document references
    compliance_notes = Column(Text)
    
    # Status tracking
    submission_date = Column(DateTime)
    approval_date = Column(DateTime)
    expiration_date = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="crypto_compliance_records")
    
    def __repr__(self):
        return f'<CryptoComplianceRecord {self.compliance_type}: {self.compliance_status}>'

# Add relationships to User model (to be added to existing user.py)
"""
Add these relationships to the User model in models/user.py:

crypto_wallets = relationship("CryptoWallet", back_populates="user", cascade="all, delete-orphan")
crypto_assets = relationship("CryptoAsset", back_populates="user", cascade="all, delete-orphan")
crypto_transactions = relationship("CryptoTransaction", back_populates="user", cascade="all, delete-orphan")
crypto_inheritance_plans = relationship("CryptoInheritancePlan", back_populates="user", cascade="all, delete-orphan")
crypto_beneficiaries = relationship("CryptoBeneficiary", back_populates="user", cascade="all, delete-orphan")
crypto_compliance_records = relationship("CryptoComplianceRecord", back_populates="user", cascade="all, delete-orphan")
"""

