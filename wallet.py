from pymongo import MongoClient
from datetime import datetime, timedelta
import os
from src.config import Config

class MongoDBConnection:
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            self._client = MongoClient(Config.MONGODB_URI)
            self._db = self._client.get_default_database()
    
    @property
    def db(self):
        return self._db
    
    @property
    def client(self):
        return self._client

# MongoDB connection instance
mongo = MongoDBConnection()

class WalletSession:
    """MongoDB model for wallet sessions"""
    
    collection_name = 'wallet_sessions'
    
    def __init__(self, data=None):
        self.data = data or {}
        self.collection = mongo.db[self.collection_name]
    
    @classmethod
    def create(cls, user_id, wallet_address, blockchain, wallet_type='external'):
        """Create a new wallet session"""
        session_data = {
            'user_id': user_id,
            'wallet_address': wallet_address,
            'blockchain': blockchain,
            'wallet_type': wallet_type,  # external, hardware, multisig
            'connected_at': datetime.utcnow(),
            'last_sync_at': datetime.utcnow(),
            'is_active': True,
            'assets': [],
            'beneficiaries': [],
            'metadata': {}
        }
        
        session = cls(session_data)
        result = session.collection.insert_one(session_data)
        session.data['_id'] = result.inserted_id
        return session
    
    @classmethod
    def find_by_user(cls, user_id):
        """Find all wallet sessions for a user"""
        sessions = []
        for doc in mongo.db[cls.collection_name].find({'user_id': user_id, 'is_active': True}):
            sessions.append(cls(doc))
        return sessions
    
    @classmethod
    def find_by_id(cls, session_id):
        """Find wallet session by ID"""
        from bson import ObjectId
        doc = mongo.db[cls.collection_name].find_one({'_id': ObjectId(session_id)})
        return cls(doc) if doc else None
    
    @classmethod
    def find_by_wallet(cls, user_id, wallet_address):
        """Find wallet session by user and wallet address"""
        doc = mongo.db[cls.collection_name].find_one({
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
        
        # Remove existing asset with same symbol/contract
        self.data['assets'] = [
            a for a in self.data['assets'] 
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
        
        # Remove existing beneficiary for same asset
        self.data['beneficiaries'] = [
            b for b in self.data['beneficiaries'] 
            if b.get('asset_symbol') != asset_symbol
        ]
        
        self.data['beneficiaries'].append(beneficiary)
        return self.save()
    
    def get_total_value(self):
        """Calculate total USD value of all assets"""
        return sum(asset.get('value_usd', 0) for asset in self.data.get('assets', []))
    
    def get_asset_count(self):
        """Get number of assets in wallet"""
        return len(self.data.get('assets', []))
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        data = self.data.copy()
        
        # Convert ObjectId to string
        if '_id' in data:
            data['_id'] = str(data['_id'])
        
        # Convert datetime objects to ISO strings
        for field in ['connected_at', 'last_sync_at', 'disconnected_at']:
            if field in data and data[field]:
                data[field] = data[field].isoformat()
        
        # Convert asset timestamps
        for asset in data.get('assets', []):
            if 'last_updated' in asset and asset['last_updated']:
                asset['last_updated'] = asset['last_updated'].isoformat()
        
        # Convert beneficiary timestamps
        for beneficiary in data.get('beneficiaries', []):
            if 'assigned_at' in beneficiary and beneficiary['assigned_at']:
                beneficiary['assigned_at'] = beneficiary['assigned_at'].isoformat()
        
        # Add computed fields
        data['total_value'] = self.get_total_value()
        data['asset_count'] = self.get_asset_count()
        
        return data

class WalletAssetCache:
    """Cache for blockchain asset data"""
    
    collection_name = 'asset_cache'
    
    def __init__(self):
        self.collection = mongo.db[self.collection_name]
    
    def get_cached_asset(self, blockchain, address, symbol):
        """Get cached asset data"""
        cache_key = f"{blockchain}:{address}:{symbol}"
        doc = self.collection.find_one({'cache_key': cache_key})
        
        if doc and doc.get('expires_at') > datetime.utcnow():
            return doc.get('data')
        
        return None
    
    def cache_asset(self, blockchain, address, symbol, data, ttl_minutes=15):
        """Cache asset data"""
        cache_key = f"{blockchain}:{address}:{symbol}"
        expires_at = datetime.utcnow() + timedelta(minutes=ttl_minutes)
        
        self.collection.update_one(
            {'cache_key': cache_key},
            {
                '$set': {
                    'cache_key': cache_key,
                    'blockchain': blockchain,
                    'address': address,
                    'symbol': symbol,
                    'data': data,
                    'cached_at': datetime.utcnow(),
                    'expires_at': expires_at
                }
            },
            upsert=True
        )
    
    def clear_expired(self):
        """Clear expired cache entries"""
        self.collection.delete_many({'expires_at': {'$lt': datetime.utcnow()}})

class BlockchainSyncLog:
    """Log for blockchain synchronization events"""
    
    collection_name = 'sync_logs'
    
    def __init__(self):
        self.collection = mongo.db[self.collection_name]
    
    def log_sync(self, user_id, wallet_address, blockchain, status, details=None):
        """Log a synchronization event"""
        log_entry = {
            'user_id': user_id,
            'wallet_address': wallet_address,
            'blockchain': blockchain,
            'status': status,  # success, error, partial
            'details': details or {},
            'timestamp': datetime.utcnow()
        }
        
        self.collection.insert_one(log_entry)
    
    def get_recent_logs(self, user_id, limit=50):
        """Get recent sync logs for a user"""
        logs = []
        for doc in self.collection.find(
            {'user_id': user_id},
            sort=[('timestamp', -1)],
            limit=limit
        ):
            doc['_id'] = str(doc['_id'])
            doc['timestamp'] = doc['timestamp'].isoformat()
            logs.append(doc)
        
        return logs

