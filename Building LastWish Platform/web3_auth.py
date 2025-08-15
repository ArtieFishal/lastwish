"""
Web3 Authentication Routes for LastWish Estate Planning Platform
Handles wallet connections, ENS resolution, and Web3 authentication
"""

from flask import Blueprint, request, jsonify, session
from flask_cors import cross_origin
import logging
import json
import re
from datetime import datetime, timedelta
from typing import Dict, Any

from models.user import User, db

# Create blueprint
web3_auth_bp = Blueprint('web3_auth', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@web3_auth_bp.route('/auth/wallet-connect', methods=['POST'])
@cross_origin()
def wallet_connect():
    """
    Handle wallet connection from frontend
    Supports MetaMask, WalletConnect, Coinbase Wallet, Trust Wallet
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'address' not in data:
            return jsonify({
                'success': False,
                'error': 'Wallet address is required'
            }), 400
        
        address = data.get('address', '').lower()
        network = data.get('network', 'ethereum')
        ens_domain = data.get('ens_domain')
        wallet_type = data.get('wallet_type', 'unknown')
        session_data = data.get('session_data')
        
        # Validate Ethereum address format
        if not re.match(r'^0x[a-fA-F0-9]{40}$', address):
            return jsonify({
                'success': False,
                'error': 'Invalid wallet address format'
            }), 400
        
        # Validate network
        supported_networks = ['ethereum', 'polygon', 'bsc', 'avalanche']
        if network not in supported_networks:
            return jsonify({
                'success': False,
                'error': f'Unsupported network: {network}'
            }), 400
        
        # Check if user exists
        user = User.query.filter_by(wallet_address=address).first()
        
        if not user:
            # Create new user
            user = User(
                wallet_address=address,
                primary_network=network,
                ens_domain=ens_domain,
                wallet_type=wallet_type,
                created_at=datetime.utcnow(),
                last_login=datetime.utcnow(),
                is_active=True
            )
            db.session.add(user)
        else:
            # Update existing user
            user.primary_network = network
            user.last_login = datetime.utcnow()
            if ens_domain:
                user.ens_domain = ens_domain
            if wallet_type:
                user.wallet_type = wallet_type
        
        # Save session data if provided (for WalletConnect)
        if session_data:
            user.wallet_session_data = json.dumps(session_data)
        
        db.session.commit()
        
        # Create session
        session['user_id'] = user.id
        session['wallet_address'] = address
        session['network'] = network
        session['authenticated'] = True
        session['auth_time'] = datetime.utcnow().isoformat()
        
        logger.info(f"Wallet connected successfully: {address} on {network}")
        
        return jsonify({
            'success': True,
            'message': 'Wallet connected successfully',
            'user': {
                'id': user.id,
                'wallet_address': user.wallet_address,
                'ens_domain': user.ens_domain,
                'primary_network': user.primary_network,
                'wallet_type': user.wallet_type,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'subscription_tier': 'free'  # Default tier
            }
        })
        
    except Exception as e:
        logger.error(f"Wallet connection error: {str(e)}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Internal server error during wallet connection'
        }), 500

@web3_auth_bp.route('/auth/resolve-ens', methods=['POST'])
@cross_origin()
def resolve_ens():
    """
    Resolve ENS domain to Ethereum address
    This is a simplified version - in production you'd use a proper ENS resolver
    """
    try:
        data = request.get_json()
        ens_domain = data.get('ens_domain', '').lower()
        
        if not ens_domain:
            return jsonify({
                'success': False,
                'error': 'ENS domain is required'
            }), 400
        
        # Validate ENS domain format
        if not ens_domain.endswith('.eth'):
            return jsonify({
                'success': False,
                'error': 'Invalid ENS domain format (must end with .eth)'
            }), 400
        
        # In a real implementation, you would:
        # 1. Connect to an Ethereum node
        # 2. Query the ENS registry
        # 3. Resolve the domain to an address
        
        # For demo purposes, we'll simulate some common ENS domains
        demo_ens_addresses = {
            'vitalik.eth': '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045',
            'nick.eth': '0xb8c2C29ee19D8307cb7255e1Cd9CbDE883A267d5',
            'brantly.eth': '0x983110309620D911731Ac0932219af06091b6744',
            'lastwish.eth': '0x742d35Cc6634C0532925a3b8D0C9C2d1234567890',
            'demo.eth': '0x1234567890123456789012345678901234567890'
        }
        
        resolved_address = demo_ens_addresses.get(ens_domain)
        
        if resolved_address:
            return jsonify({
                'success': True,
                'ens_domain': ens_domain,
                'resolved_address': resolved_address,
                'message': f'Successfully resolved {ens_domain}'
            })
        else:
            # In production, you would actually query ENS here
            # For now, return a simulated "not found" response
            return jsonify({
                'success': False,
                'error': f'ENS domain {ens_domain} not found or not registered'
            }), 404
            
    except Exception as e:
        logger.error(f"ENS resolution error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error during ENS resolution'
        }), 500

@web3_auth_bp.route('/auth/status', methods=['GET'])
@cross_origin()
def auth_status():
    """
    Check current authentication status
    """
    try:
        if 'user_id' in session and session.get('authenticated'):
            user = User.query.get(session['user_id'])
            if user and user.is_active:
                return jsonify({
                    'authenticated': True,
                    'user': {
                        'id': user.id,
                        'wallet_address': user.wallet_address,
                        'ens_domain': user.ens_domain,
                        'primary_network': user.primary_network,
                        'wallet_type': user.wallet_type,
                        'subscription_tier': 'free'  # Default tier
                    }
                })
        
        return jsonify({
            'authenticated': False,
            'user': None
        })
        
    except Exception as e:
        logger.error(f"Auth status check error: {str(e)}")
        return jsonify({
            'authenticated': False,
            'user': None,
            'error': 'Error checking authentication status'
        }), 500

@web3_auth_bp.route('/auth/disconnect', methods=['POST'])
@cross_origin()
def disconnect_wallet():
    """
    Disconnect wallet and clear session
    """
    try:
        # Clear session
        session.clear()
        
        return jsonify({
            'success': True,
            'message': 'Wallet disconnected successfully'
        })
        
    except Exception as e:
        logger.error(f"Wallet disconnect error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error disconnecting wallet'
        }), 500

@web3_auth_bp.route('/auth/networks', methods=['GET'])
@cross_origin()
def get_supported_networks():
    """
    Get list of supported blockchain networks
    """
    try:
        networks = {
            'ethereum': {
                'name': 'Ethereum',
                'chain_id': 1,
                'currency': 'ETH',
                'rpc_url': 'https://mainnet.infura.io/v3/',
                'explorer': 'https://etherscan.io'
            },
            'polygon': {
                'name': 'Polygon',
                'chain_id': 137,
                'currency': 'MATIC',
                'rpc_url': 'https://polygon-rpc.com/',
                'explorer': 'https://polygonscan.com'
            },
            'bsc': {
                'name': 'Binance Smart Chain',
                'chain_id': 56,
                'currency': 'BNB',
                'rpc_url': 'https://bsc-dataseed.binance.org/',
                'explorer': 'https://bscscan.com'
            },
            'avalanche': {
                'name': 'Avalanche',
                'chain_id': 43114,
                'currency': 'AVAX',
                'rpc_url': 'https://api.avax.network/ext/bc/C/rpc',
                'explorer': 'https://snowtrace.io'
            }
        }
        
        return jsonify({
            'success': True,
            'networks': networks
        })
        
    except Exception as e:
        logger.error(f"Get networks error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error retrieving supported networks'
        }), 500

@web3_auth_bp.route('/auth/verify-signature', methods=['POST'])
@cross_origin()
def verify_signature():
    """
    Verify wallet signature for enhanced security
    Used for sensitive operations like will creation
    """
    try:
        data = request.get_json()
        
        address = data.get('address')
        signature = data.get('signature')
        message = data.get('message')
        
        if not all([address, signature, message]):
            return jsonify({
                'success': False,
                'error': 'Address, signature, and message are required'
            }), 400
        
        # In a real implementation, you would:
        # 1. Verify the signature using cryptographic libraries
        # 2. Ensure the message matches expected format
        # 3. Check that the signature was created by the claimed address
        
        # For demo purposes, we'll simulate signature verification
        # In production, use libraries like eth-account or web3.py
        
        # Simulate successful verification
        is_valid = True  # In production: verify_eth_signature(message, signature, address)
        
        if is_valid:
            return jsonify({
                'success': True,
                'verified': True,
                'message': 'Signature verified successfully'
            })
        else:
            return jsonify({
                'success': False,
                'verified': False,
                'error': 'Invalid signature'
            }), 400
            
    except Exception as e:
        logger.error(f"Signature verification error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error verifying signature'
        }), 500

# Helper function to check if user is authenticated
def require_auth(f):
    """
    Decorator to require authentication for protected routes
    """
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or not session.get('authenticated'):
            return jsonify({
                'success': False,
                'error': 'Authentication required'
            }), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Helper function to get current user
def get_current_user():
    """
    Get current authenticated user
    """
    if 'user_id' in session and session.get('authenticated'):
        return User.query.get(session['user_id'])
    return None

