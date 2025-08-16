from pymongo import MongoClient
from datetime import datetime, timedelta
from flask import g, current_app

def get_db():
    """
    Opens a new database connection if there is none yet for the
    current application context.
    """
    if 'db' not in g:
        g.db = MongoClient(current_app.config['MONGODB_URI'])
    return g.db.get_default_database()

class WalletSession:
    """MongoDB model for wallet sessions"""

    collection_name = 'wallet_sessions'

    def __init__(self, data=None):
        self.data = data or {}
        self.db = get_db()
        self.collection = self.db[self.collection_name]

    @classmethod
    def create(cls, user_id, wallet_address, blockchain, wallet_type='external'):
        """Create a new wallet session"""
        db = get_db()
        collection = db[cls.collection_name]

        session_data = {
            'user_id': user_id,
            'wallet_address': wallet_address,
            'blockchain': blockchain,
            'wallet_type': wallet_type,
            'connected_at': datetime.utcnow(),
            'last_sync_at': datetime.utcnow(),
            'is_active': True,
            'assets': [],
            'beneficiaries': [],
            'metadata': {}
        }

        result = collection.insert_one(session_data)
        session_data['_id'] = result.inserted_id
        return cls(session_data)

    @classmethod
    def find_by_user(cls, user_id):
        """Find all wallet sessions for a user"""
        db = get_db()
        collection = db[cls.collection_name]
        sessions = []
        for doc in collection.find({'user_id': user_id, 'is_active': True}):
            sessions.append(cls(doc))
        return sessions

    @classmethod
    def find_by_id(cls, session_id):
        """Find wallet session by ID"""
        from bson import ObjectId
        db = get_db()
        collection = db[cls.collection_name]
        doc = collection.find_one({'_id': ObjectId(session_id)})
        return cls(doc) if doc else None

    @classmethod
    def find_by_wallet(cls, user_id, wallet_address):
        """Find wallet session by user and wallet address"""
        db = get_db()
        collection = db[cls.collection_name]
        doc = collection.find_one({
            'user_id': user_id,
            'wallet_address': wallet_address,
            'is_active': True
        })
        return cls(doc) if doc else None

    def save(self):
        """Save the wallet session"""
        if '_id' in self.data:
            self.collection.update_one(
                {'_id': self.data['_id']},
                {'$set': self.data}
            )
        else:
            result = self.collection.insert_one(self.data)
            self.data['_id'] = result.inserted_id
        return self

    def delete(self):
        """Delete the wallet session"""
        if '_id' in self.data:
            self.collection.delete_one({'_id': self.data['_id']})

    def disconnect(self):
        """Mark wallet session as disconnected"""
        self.data['is_active'] = False
        self.data['disconnected_at'] = datetime.utcnow()
        return self.save()

    def add_asset(self, asset_data):
        """Add an asset to the wallet session"""
        asset = {
            'symbol': asset_data.get('symbol'),
            'name': asset_data.get('name'),
            'balance': asset_data.get('balance'),
            'value_usd': asset_data.get('value_usd'),
            'contract_address': asset_data.get('contract_address'),
            'token_type': asset_data.get('token_type', 'unknown'),
            'decimals': asset_data.get('decimals'),
            'logo_url': asset_data.get('logo_url'),
            'last_updated': datetime.utcnow()
        }

        self.data['assets'] = [
            a for a in self.data.get('assets', [])
            if not (a.get('symbol') == asset['symbol'] and
                   a.get('contract_address') == asset.get('contract_address'))
        ]

        self.data['assets'].append(asset)
        self.data['last_sync_at'] = datetime.utcnow()
        return self.save()

    def update_assets(self, assets_list):
        """Update all assets for the wallet"""
        self.data['assets'] = []
        for asset_data in assets_list:
            self.add_asset(asset_data)
        return self

    def assign_beneficiary(self, asset_symbol, beneficiary_data):
        """Assign a beneficiary to an asset"""
        beneficiary = {
            'asset_symbol': asset_symbol,
            'name': beneficiary_data.get('name'),
            'email': beneficiary_data.get('email'),
            'relationship': beneficiary_data.get('relationship'),
            'percentage': beneficiary_data.get('percentage', 100),
            'assigned_at': datetime.utcnow()
        }

        self.data['beneficiaries'] = [
            b for b in self.data.get('beneficiaries', [])
            if b.get('asset_symbol') != asset_symbol
        ]

        self.data['beneficiaries'].append(beneficiary)
        return self.save()

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        data = self.data.copy()

        if '_id' in data:
            data['_id'] = str(data['_id'])

        for field in ['connected_at', 'last_sync_at', 'disconnected_at']:
            if field in data and data.get(field):
                data[field] = data[field].isoformat()

        for asset in data.get('assets', []):
            if 'last_updated' in asset and asset.get('last_updated'):
                asset['last_updated'] = asset['last_updated'].isoformat()

        for beneficiary in data.get('beneficiaries', []):
            if 'assigned_at' in beneficiary and beneficiary.get('assigned_at'):
                beneficiary['assigned_at'] = beneficiary['assigned_at'].isoformat()

        return data

# Note: The other classes (WalletAssetCache, BlockchainSyncLog) would be refactored similarly,
# but are omitted here for brevity as they are not used by the current API endpoints.
