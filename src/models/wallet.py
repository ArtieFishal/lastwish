from pymongo import MongoClient
from datetime import datetime
from flask import g, current_app

def get_db():
    if 'db' not in g:
        g.db_client = MongoClient(current_app.config['MONGODB_URI'])
        g.db = g.db_client.get_default_database()
    return g.db

class WalletSession:
    collection_name = 'wallet_sessions'

    @staticmethod
    def get_collection():
        db = get_db()
        return db[WalletSession.collection_name]

    @classmethod
    def create(cls, user_id, wallet_address, blockchain, wallet_type='external'):
        collection = cls.get_collection()
        session_data = {
            'user_id': user_id, 'wallet_address': wallet_address, 'blockchain': blockchain,
            'wallet_type': wallet_type, 'connected_at': datetime.utcnow(),
            'last_sync_at': datetime.utcnow(), 'is_active': True,
            'assets': [], 'beneficiaries': [],
        }
        result = collection.insert_one(session_data)
        session_data['_id'] = result.inserted_id
        return session_data

    @classmethod
    def find_by_wallet(cls, user_id, wallet_address):
        collection = cls.get_collection()
        return collection.find_one({'user_id': user_id, 'wallet_address': wallet_address})

    @classmethod
    def find_by_user(cls, user_id):
        collection = cls.get_collection()
        return list(collection.find({'user_id': user_id}))

    @staticmethod
    def update(wallet_id, data):
        collection = WalletSession.get_collection()
        collection.update_one({'_id': wallet_id}, {'$set': data})

    @staticmethod
    def add_assets(wallet_id, assets_list):
        collection = WalletSession.get_collection()
        collection.update_one({'_id': wallet_id}, {'$set': {'assets': assets_list, 'last_sync_at': datetime.utcnow()}})

    @staticmethod
    def add_beneficiary(wallet_id, beneficiary_data):
        collection = WalletSession.get_collection()
        collection.update_one({'_id': wallet_id}, {'$push': {'beneficiaries': beneficiary_data}})

def to_json(data):
    """Custom JSON encoder for MongoDB data"""
    if not data:
        return None
    if isinstance(data, list):
        return [to_json(item) for item in data]

    data['_id'] = str(data['_id'])
    # Convert other non-serializable fields like datetime if necessary
    return data
