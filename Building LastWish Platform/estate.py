from src.models.user import db
from datetime import datetime
from enum import Enum
import json

class DocumentStatus(Enum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    EXECUTED = "executed"
    ARCHIVED = "archived"

class AssetType(Enum):
    REAL_ESTATE = "real_estate"
    BANK_ACCOUNT = "bank_account"
    INVESTMENT = "investment"
    INSURANCE = "insurance"
    VEHICLE = "vehicle"
    PERSONAL_PROPERTY = "personal_property"
    BUSINESS_INTEREST = "business_interest"
    DIGITAL_ASSET = "digital_asset"
    CRYPTOCURRENCY = "cryptocurrency"

class RelationshipType(Enum):
    SPOUSE = "spouse"
    CHILD = "child"
    PARENT = "parent"
    SIBLING = "sibling"
    GRANDCHILD = "grandchild"
    FRIEND = "friend"
    ORGANIZATION = "organization"
    OTHER = "other"

class Will(db.Model):
    __tablename__ = 'wills'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False, default="Last Will and Testament")
    status = db.Column(db.Enum(DocumentStatus), default=DocumentStatus.DRAFT)
    
    # Personal Information
    testator_full_name = db.Column(db.String(200))
    testator_address = db.Column(db.Text)
    testator_date_of_birth = db.Column(db.Date)
    testator_ssn_last_four = db.Column(db.String(4))
    
    # Executor Information
    executor_id = db.Column(db.Integer, db.ForeignKey('beneficiaries.id'))
    alternate_executor_id = db.Column(db.Integer, db.ForeignKey('beneficiaries.id'))
    
    # Guardian Information (for minor children)
    guardian_id = db.Column(db.Integer, db.ForeignKey('beneficiaries.id'))
    alternate_guardian_id = db.Column(db.Integer, db.ForeignKey('beneficiaries.id'))
    
    # Document Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    executed_at = db.Column(db.DateTime)
    
    # Legal Execution
    witness_1_signature = db.Column(db.Text)  # Digital signature data
    witness_2_signature = db.Column(db.Text)
    notary_signature = db.Column(db.Text)
    testator_signature = db.Column(db.Text)
    
    # Additional Instructions
    funeral_instructions = db.Column(db.Text)
    burial_instructions = db.Column(db.Text)
    special_instructions = db.Column(db.Text)
    
    # Relationships
    user = db.relationship('User', backref='wills')
    executor = db.relationship('Beneficiary', foreign_keys=[executor_id], backref='executor_wills')
    alternate_executor = db.relationship('Beneficiary', foreign_keys=[alternate_executor_id], backref='alt_executor_wills')
    guardian = db.relationship('Beneficiary', foreign_keys=[guardian_id], backref='guardian_wills')
    alternate_guardian = db.relationship('Beneficiary', foreign_keys=[alternate_guardian_id], backref='alt_guardian_wills')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'status': self.status.value if self.status else None,
            'testator_full_name': self.testator_full_name,
            'testator_address': self.testator_address,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'executed_at': self.executed_at.isoformat() if self.executed_at else None,
            'executor_id': self.executor_id,
            'guardian_id': self.guardian_id,
            'funeral_instructions': self.funeral_instructions,
            'burial_instructions': self.burial_instructions,
            'special_instructions': self.special_instructions
        }

class Beneficiary(db.Model):
    __tablename__ = 'beneficiaries'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Personal Information
    full_name = db.Column(db.String(200), nullable=False)
    relationship = db.Column(db.Enum(RelationshipType), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    date_of_birth = db.Column(db.Date)
    ssn_last_four = db.Column(db.String(4))
    
    # Organization Information (for charities, etc.)
    organization_name = db.Column(db.String(200))
    tax_id = db.Column(db.String(20))
    
    # Status
    is_primary = db.Column(db.Boolean, default=True)
    is_contingent = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='beneficiaries')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'full_name': self.full_name,
            'relationship': self.relationship.value if self.relationship else None,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'organization_name': self.organization_name,
            'tax_id': self.tax_id,
            'is_primary': self.is_primary,
            'is_contingent': self.is_contingent,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Asset(db.Model):
    __tablename__ = 'assets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    will_id = db.Column(db.Integer, db.ForeignKey('wills.id'))
    
    # Asset Information
    name = db.Column(db.String(200), nullable=False)
    asset_type = db.Column(db.Enum(AssetType), nullable=False)
    description = db.Column(db.Text)
    estimated_value = db.Column(db.Numeric(15, 2))
    
    # Location/Account Information
    location = db.Column(db.Text)  # Address for real estate, account number for financial
    institution_name = db.Column(db.String(200))  # Bank, brokerage, etc.
    account_number = db.Column(db.String(100))
    
    # Legal Information
    deed_title_info = db.Column(db.Text)
    liens_mortgages = db.Column(db.Text)
    
    # Digital Asset Specific
    login_credentials = db.Column(db.Text)  # Encrypted
    recovery_information = db.Column(db.Text)  # Encrypted
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='assets')
    will = db.relationship('Will', backref='assets')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'will_id': self.will_id,
            'name': self.name,
            'asset_type': self.asset_type.value if self.asset_type else None,
            'description': self.description,
            'estimated_value': float(self.estimated_value) if self.estimated_value else None,
            'location': self.location,
            'institution_name': self.institution_name,
            'account_number': self.account_number,
            'deed_title_info': self.deed_title_info,
            'liens_mortgages': self.liens_mortgages,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class AssetDistribution(db.Model):
    __tablename__ = 'asset_distributions'
    
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=False)
    beneficiary_id = db.Column(db.Integer, db.ForeignKey('beneficiaries.id'), nullable=False)
    
    # Distribution Details
    percentage = db.Column(db.Numeric(5, 2))  # 0.00 to 100.00
    specific_amount = db.Column(db.Numeric(15, 2))
    conditions = db.Column(db.Text)  # Age requirements, milestones, etc.
    
    # Priority
    is_primary = db.Column(db.Boolean, default=True)
    is_contingent = db.Column(db.Boolean, default=False)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    asset = db.relationship('Asset', backref='distributions')
    beneficiary = db.relationship('Beneficiary', backref='asset_distributions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'asset_id': self.asset_id,
            'beneficiary_id': self.beneficiary_id,
            'percentage': float(self.percentage) if self.percentage else None,
            'specific_amount': float(self.specific_amount) if self.specific_amount else None,
            'conditions': self.conditions,
            'is_primary': self.is_primary,
            'is_contingent': self.is_contingent,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class DigitalAsset(db.Model):
    __tablename__ = 'digital_assets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Platform Information
    platform_name = db.Column(db.String(100), nullable=False)  # Facebook, Gmail, etc.
    account_type = db.Column(db.String(50))  # social_media, email, financial, etc.
    username = db.Column(db.String(100))
    email_associated = db.Column(db.String(120))
    
    # Access Information (Encrypted)
    login_credentials = db.Column(db.Text)  # Encrypted JSON
    recovery_codes = db.Column(db.Text)  # Encrypted
    two_factor_backup = db.Column(db.Text)  # Encrypted
    
    # Instructions
    action_on_death = db.Column(db.String(50))  # delete, memorialize, transfer, etc.
    special_instructions = db.Column(db.Text)
    designated_contact_id = db.Column(db.Integer, db.ForeignKey('beneficiaries.id'))
    
    # Value Information
    estimated_value = db.Column(db.Numeric(15, 2))
    contains_valuable_data = db.Column(db.Boolean, default=False)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='digital_assets')
    designated_contact = db.relationship('Beneficiary', backref='digital_asset_contacts')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'platform_name': self.platform_name,
            'account_type': self.account_type,
            'username': self.username,
            'email_associated': self.email_associated,
            'action_on_death': self.action_on_death,
            'special_instructions': self.special_instructions,
            'designated_contact_id': self.designated_contact_id,
            'estimated_value': float(self.estimated_value) if self.estimated_value else None,
            'contains_valuable_data': self.contains_valuable_data,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class PowerOfAttorney(db.Model):
    __tablename__ = 'power_of_attorney'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Document Information
    document_type = db.Column(db.String(50))  # financial, healthcare, general
    status = db.Column(db.Enum(DocumentStatus), default=DocumentStatus.DRAFT)
    
    # Agent Information
    agent_id = db.Column(db.Integer, db.ForeignKey('beneficiaries.id'), nullable=False)
    alternate_agent_id = db.Column(db.Integer, db.ForeignKey('beneficiaries.id'))
    
    # Powers and Limitations
    powers_granted = db.Column(db.Text)  # JSON array of specific powers
    limitations = db.Column(db.Text)
    effective_date = db.Column(db.Date)
    expiration_date = db.Column(db.Date)
    
    # Execution Information
    is_durable = db.Column(db.Boolean, default=True)
    requires_incapacity = db.Column(db.Boolean, default=False)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    executed_at = db.Column(db.DateTime)
    
    # Relationships
    user = db.relationship('User', backref='power_of_attorney_docs')
    agent = db.relationship('Beneficiary', foreign_keys=[agent_id], backref='poa_agent_docs')
    alternate_agent = db.relationship('Beneficiary', foreign_keys=[alternate_agent_id], backref='poa_alt_agent_docs')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'document_type': self.document_type,
            'status': self.status.value if self.status else None,
            'agent_id': self.agent_id,
            'alternate_agent_id': self.alternate_agent_id,
            'powers_granted': self.powers_granted,
            'limitations': self.limitations,
            'effective_date': self.effective_date.isoformat() if self.effective_date else None,
            'expiration_date': self.expiration_date.isoformat() if self.expiration_date else None,
            'is_durable': self.is_durable,
            'requires_incapacity': self.requires_incapacity,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'executed_at': self.executed_at.isoformat() if self.executed_at else None
        }

class HealthDirective(db.Model):
    __tablename__ = 'health_directives'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Document Information
    status = db.Column(db.Enum(DocumentStatus), default=DocumentStatus.DRAFT)
    
    # Healthcare Agent
    healthcare_agent_id = db.Column(db.Integer, db.ForeignKey('beneficiaries.id'))
    alternate_agent_id = db.Column(db.Integer, db.ForeignKey('beneficiaries.id'))
    
    # Medical Preferences
    life_sustaining_treatment = db.Column(db.String(50))  # continue, discontinue, agent_decides
    artificial_nutrition = db.Column(db.String(50))
    pain_management = db.Column(db.String(50))
    organ_donation = db.Column(db.Boolean)
    tissue_donation = db.Column(db.Boolean)
    
    # Specific Instructions
    medical_conditions = db.Column(db.Text)
    treatment_preferences = db.Column(db.Text)
    religious_considerations = db.Column(db.Text)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    executed_at = db.Column(db.DateTime)
    
    # Relationships
    user = db.relationship('User', backref='health_directives')
    healthcare_agent = db.relationship('Beneficiary', foreign_keys=[healthcare_agent_id], backref='healthcare_agent_docs')
    alternate_agent = db.relationship('Beneficiary', foreign_keys=[alternate_agent_id], backref='healthcare_alt_agent_docs')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'status': self.status.value if self.status else None,
            'healthcare_agent_id': self.healthcare_agent_id,
            'alternate_agent_id': self.alternate_agent_id,
            'life_sustaining_treatment': self.life_sustaining_treatment,
            'artificial_nutrition': self.artificial_nutrition,
            'pain_management': self.pain_management,
            'organ_donation': self.organ_donation,
            'tissue_donation': self.tissue_donation,
            'medical_conditions': self.medical_conditions,
            'treatment_preferences': self.treatment_preferences,
            'religious_considerations': self.religious_considerations,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'executed_at': self.executed_at.isoformat() if self.executed_at else None
        }

class DocumentAccess(db.Model):
    __tablename__ = 'document_access'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    beneficiary_id = db.Column(db.Integer, db.ForeignKey('beneficiaries.id'), nullable=False)
    
    # Access Permissions
    can_view_will = db.Column(db.Boolean, default=False)
    can_view_assets = db.Column(db.Boolean, default=False)
    can_view_digital_assets = db.Column(db.Boolean, default=False)
    can_view_health_directive = db.Column(db.Boolean, default=False)
    
    # Access Conditions
    access_after_death_only = db.Column(db.Boolean, default=True)
    access_after_incapacity = db.Column(db.Boolean, default=False)
    immediate_access = db.Column(db.Boolean, default=False)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='document_access_grants')
    beneficiary = db.relationship('Beneficiary', backref='document_access_permissions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'beneficiary_id': self.beneficiary_id,
            'can_view_will': self.can_view_will,
            'can_view_assets': self.can_view_assets,
            'can_view_digital_assets': self.can_view_digital_assets,
            'can_view_health_directive': self.can_view_health_directive,
            'access_after_death_only': self.access_after_death_only,
            'access_after_incapacity': self.access_after_incapacity,
            'immediate_access': self.immediate_access,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Action Information
    action = db.Column(db.String(100), nullable=False)  # created, updated, deleted, viewed, executed
    resource_type = db.Column(db.String(50), nullable=False)  # will, asset, beneficiary, etc.
    resource_id = db.Column(db.Integer)
    
    # Details
    description = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='audit_logs')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'description': self.description,
            'ip_address': self.ip_address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

