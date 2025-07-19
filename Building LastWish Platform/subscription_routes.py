"""
Subscription and Payment API Routes for LastWish Estate Planning Platform
Handles subscription management, billing, and payment processing
"""

from flask import Blueprint, request, jsonify, session
from flask_cors import cross_origin
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, Any

from models.user import User, db
from models.subscription_models import (
    SubscriptionTier, UserSubscription, Payment, PromoCode, UsageLog,
    get_user_subscription, check_feature_limit, log_feature_usage
)

# Create blueprint
subscription_bp = Blueprint('subscription', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create blueprint for subscription routes
subscription_bp = Blueprint('subscription', __name__, url_prefix='/api/subscription')

@subscription_bp.route('/health', methods=['GET'])
@cross_origin()
def health_check():
    """Health check endpoint for subscription service"""
    return jsonify({
        'status': 'healthy',
        'service': 'subscription_management',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@subscription_bp.route('/tiers', methods=['GET'])
@cross_origin()
def get_subscription_tiers():
    """
    Get all available subscription tiers with features and pricing
    """
    try:
        tiers = SubscriptionTier.query.filter_by(is_active=True).order_by(SubscriptionTier.sort_order).all()
        
        tiers_data = []
        for tier in tiers:
            tier_data = tier.to_dict()
            
            # Add popular/recommended flags
            if tier.name == 'basic':
                tier_data['is_popular'] = True
            elif tier.name == 'premium':
                tier_data['is_recommended'] = True
            
            # Calculate yearly savings
            if tier.price_yearly > 0 and tier.price_monthly > 0:
                yearly_equivalent = tier.price_monthly * 12
                savings = yearly_equivalent - tier.price_yearly
                tier_data['yearly_savings'] = savings
                tier_data['yearly_savings_percentage'] = round((savings / yearly_equivalent) * 100, 1)
            
            tiers_data.append(tier_data)
        
        return jsonify({
            'success': True,
            'tiers': tiers_data,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Failed to get subscription tiers: {str(e)}")
        return jsonify({
            'error': 'Failed to get subscription tiers',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@subscription_bp.route('/current', methods=['GET'])
@cross_origin()
def get_current_subscription():
    """
    Get current user's subscription details and usage
    """
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User authentication required'}), 401
        
        subscription = get_user_subscription(user_id)
        
        if not subscription:
            # User has no subscription - return free tier info
            free_tier = SubscriptionTier.query.filter_by(name='free').first()
            return jsonify({
                'success': True,
                'subscription': None,
                'tier': free_tier.to_dict() if free_tier else None,
                'is_free_user': True,
                'usage': {
                    'wills_used': 0,
                    'assets_used': 0,
                    'crypto_assets_used': 0,
                    'beneficiaries_used': 0,
                    'smart_contracts_used': 0,
                    'ai_queries_used': 0
                },
                'timestamp': datetime.now().isoformat()
            })
        
        # Calculate usage percentages
        usage_percentages = {}
        for feature in ['wills', 'assets', 'crypto_assets', 'beneficiaries', 'smart_contracts']:
            usage_percentages[f'{feature}_percentage'] = subscription.usage_percentage(feature)
        
        return jsonify({
            'success': True,
            'subscription': subscription.to_dict(),
            'tier': subscription.tier.to_dict(),
            'is_free_user': False,
            'usage_percentages': usage_percentages,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Failed to get current subscription: {str(e)}")
        return jsonify({
            'error': 'Failed to get current subscription',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@subscription_bp.route('/upgrade', methods=['POST'])
@cross_origin()
def upgrade_subscription():
    """
    Upgrade user's subscription to a new tier
    """
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User authentication required'}), 401
        
        data = request.get_json()
        tier_id = data.get('tier_id')
        billing_cycle = data.get('billing_cycle', 'monthly')
        payment_method = data.get('payment_method', 'stripe')
        promo_code = data.get('promo_code')
        
        if not tier_id:
            return jsonify({'error': 'Tier ID is required'}), 400
        
        # Get target tier
        target_tier = SubscriptionTier.query.get(tier_id)
        if not target_tier or not target_tier.is_active:
            return jsonify({'error': 'Invalid subscription tier'}), 400
        
        # Get user
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Calculate pricing
        if billing_cycle == 'yearly':
            amount = target_tier.price_yearly
        else:
            amount = target_tier.price_monthly
        
        # Apply promo code if provided
        discount_amount = 0.0
        promo = None
        if promo_code:
            promo = PromoCode.query.filter_by(code=promo_code.upper()).first()
            if promo and promo.is_valid():
                discount_amount = promo.calculate_discount(amount)
                amount -= discount_amount
        
        # Check for existing subscription
        existing_subscription = get_user_subscription(user_id)
        
        # Calculate subscription dates
        start_date = datetime.now()
        if billing_cycle == 'yearly':
            end_date = start_date + timedelta(days=365)
            next_billing_date = end_date
        else:
            end_date = start_date + timedelta(days=30)
            next_billing_date = end_date
        
        # Create or update subscription
        if existing_subscription:
            # Update existing subscription
            existing_subscription.tier_id = tier_id
            existing_subscription.billing_cycle = billing_cycle
            existing_subscription.status = 'active'
            existing_subscription.start_date = start_date
            existing_subscription.end_date = end_date
            existing_subscription.next_billing_date = next_billing_date
            existing_subscription.amount_paid = amount
            existing_subscription.payment_method = payment_method
            existing_subscription.updated_at = datetime.now()
            subscription = existing_subscription
        else:
            # Create new subscription
            subscription = UserSubscription(
                user_id=user_id,
                tier_id=tier_id,
                status='active',
                billing_cycle=billing_cycle,
                start_date=start_date,
                end_date=end_date,
                next_billing_date=next_billing_date,
                amount_paid=amount,
                payment_method=payment_method
            )
            db.session.add(subscription)
        
        # Create payment record
        payment = Payment(
            user_id=user_id,
            amount=amount + discount_amount,  # Original amount
            currency='USD',
            payment_method=payment_method,
            status='completed',  # Simulated successful payment
            billing_period_start=start_date,
            billing_period_end=end_date,
            description=f'{target_tier.display_name} subscription ({billing_cycle})',
            processed_at=datetime.now()
        )
        
        # Add discount information if promo code was used
        if discount_amount > 0:
            payment.description += f' - Promo code {promo_code} applied (${discount_amount:.2f} discount)'
        
        db.session.add(payment)
        
        # Update payment with subscription ID after commit
        db.session.flush()
        payment.subscription_id = subscription.id
        
        # Update promo code usage
        if promo:
            promo.current_uses += 1
        
        # Update user subscription tier
        user.subscription_tier = target_tier.name
        
        db.session.commit()
        
        # Log the subscription upgrade
        log_feature_usage(
            user_id=user_id,
            feature='subscription',
            action='upgrade',
            resource_id=str(subscription.id),
            metadata=json.dumps({
                'tier_name': target_tier.name,
                'billing_cycle': billing_cycle,
                'amount_paid': amount,
                'promo_code': promo_code if promo_code else None,
                'discount_amount': discount_amount
            })
        )
        
        logger.info(f"Subscription upgraded for user {user_id} to {target_tier.name}")
        
        return jsonify({
            'success': True,
            'subscription': subscription.to_dict(),
            'payment': payment.to_dict(),
            'message': f'Successfully upgraded to {target_tier.display_name}!',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Subscription upgrade failed: {str(e)}")
        return jsonify({
            'error': 'Subscription upgrade failed',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@subscription_bp.route('/cancel', methods=['POST'])
@cross_origin()
def cancel_subscription():
    """
    Cancel user's current subscription
    """
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User authentication required'}), 401
        
        data = request.get_json()
        cancellation_reason = data.get('reason', 'User requested cancellation')
        immediate = data.get('immediate', False)
        
        subscription = get_user_subscription(user_id)
        if not subscription:
            return jsonify({'error': 'No active subscription found'}), 404
        
        # Update subscription status
        if immediate:
            subscription.status = 'cancelled'
            subscription.end_date = datetime.now()
        else:
            # Cancel at end of billing period
            subscription.auto_renew = False
            subscription.status = 'cancelled'
        
        subscription.cancelled_at = datetime.now()
        subscription.cancellation_reason = cancellation_reason
        subscription.updated_at = datetime.now()
        
        # Update user tier to free
        user = User.query.get(user_id)
        if user:
            user.subscription_tier = 'free'
        
        db.session.commit()
        
        # Log the cancellation
        log_feature_usage(
            user_id=user_id,
            feature='subscription',
            action='cancel',
            resource_id=str(subscription.id),
            metadata=json.dumps({
                'reason': cancellation_reason,
                'immediate': immediate,
                'cancelled_at': subscription.cancelled_at.isoformat()
            })
        )
        
        logger.info(f"Subscription cancelled for user {user_id}")
        
        return jsonify({
            'success': True,
            'subscription': subscription.to_dict(),
            'message': 'Subscription cancelled successfully',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Subscription cancellation failed: {str(e)}")
        return jsonify({
            'error': 'Subscription cancellation failed',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@subscription_bp.route('/validate-promo', methods=['POST'])
@cross_origin()
def validate_promo_code():
    """
    Validate a promotional code and calculate discount
    """
    try:
        data = request.get_json()
        promo_code = data.get('promo_code', '').strip().upper()
        tier_id = data.get('tier_id')
        billing_cycle = data.get('billing_cycle', 'monthly')
        
        if not promo_code:
            return jsonify({'error': 'Promo code is required'}), 400
        
        if not tier_id:
            return jsonify({'error': 'Tier ID is required'}), 400
        
        # Get promo code
        promo = PromoCode.query.filter_by(code=promo_code).first()
        if not promo:
            return jsonify({
                'valid': False,
                'error': 'Invalid promo code',
                'timestamp': datetime.now().isoformat()
            })
        
        # Check if promo code is valid
        if not promo.is_valid():
            return jsonify({
                'valid': False,
                'error': 'Promo code has expired or reached usage limit',
                'timestamp': datetime.now().isoformat()
            })
        
        # Get tier pricing
        tier = SubscriptionTier.query.get(tier_id)
        if not tier:
            return jsonify({'error': 'Invalid tier ID'}), 400
        
        original_amount = tier.price_yearly if billing_cycle == 'yearly' else tier.price_monthly
        discount_amount = promo.calculate_discount(original_amount)
        final_amount = original_amount - discount_amount
        
        return jsonify({
            'valid': True,
            'promo_code': promo.to_dict(),
            'pricing': {
                'original_amount': original_amount,
                'discount_amount': discount_amount,
                'final_amount': final_amount,
                'savings_percentage': round((discount_amount / original_amount) * 100, 1) if original_amount > 0 else 0
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Promo code validation failed: {str(e)}")
        return jsonify({
            'error': 'Promo code validation failed',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@subscription_bp.route('/usage', methods=['GET'])
@cross_origin()
def get_usage_stats():
    """
    Get detailed usage statistics for current user
    """
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User authentication required'}), 401
        
        subscription = get_user_subscription(user_id)
        
        # Get usage logs for the current month
        start_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        usage_logs = UsageLog.query.filter(
            UsageLog.user_id == user_id,
            UsageLog.timestamp >= start_of_month
        ).all()
        
        # Aggregate usage by feature
        usage_by_feature = {}
        for log in usage_logs:
            if log.feature not in usage_by_feature:
                usage_by_feature[log.feature] = {
                    'total_actions': 0,
                    'actions_by_type': {}
                }
            
            usage_by_feature[log.feature]['total_actions'] += 1
            
            if log.action not in usage_by_feature[log.feature]['actions_by_type']:
                usage_by_feature[log.feature]['actions_by_type'][log.action] = 0
            usage_by_feature[log.feature]['actions_by_type'][log.action] += 1
        
        # Get subscription limits and current usage
        limits = {}
        current_usage = {}
        usage_percentages = {}
        
        if subscription:
            for feature in ['wills', 'assets', 'crypto_assets', 'beneficiaries', 'smart_contracts']:
                limit = getattr(subscription.tier, f'max_{feature}', 0)
                used = getattr(subscription, f'{feature}_used', 0)
                
                limits[feature] = limit if limit > 0 else 'Unlimited'
                current_usage[feature] = used
                usage_percentages[feature] = subscription.usage_percentage(feature)
        else:
            # Free tier limits
            free_tier = SubscriptionTier.query.filter_by(name='free').first()
            if free_tier:
                for feature in ['wills', 'assets', 'crypto_assets', 'beneficiaries', 'smart_contracts']:
                    limit = getattr(free_tier, f'max_{feature}', 0)
                    limits[feature] = limit if limit > 0 else 'Unlimited'
                    current_usage[feature] = 0
                    usage_percentages[feature] = 0
        
        return jsonify({
            'success': True,
            'subscription_id': subscription.id if subscription else None,
            'tier_name': subscription.tier.name if subscription else 'free',
            'limits': limits,
            'current_usage': current_usage,
            'usage_percentages': usage_percentages,
            'monthly_activity': usage_by_feature,
            'billing_period': {
                'start': subscription.start_date.isoformat() if subscription and subscription.start_date else None,
                'end': subscription.end_date.isoformat() if subscription and subscription.end_date else None,
                'days_remaining': subscription.days_remaining() if subscription else None
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Failed to get usage stats: {str(e)}")
        return jsonify({
            'error': 'Failed to get usage stats',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@subscription_bp.route('/check-limit/<feature>', methods=['GET'])
@cross_origin()
def check_feature_limit_endpoint(feature):
    """
    Check if user can use a specific feature based on subscription limits
    """
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User authentication required'}), 401
        
        count = request.args.get('count', 1, type=int)
        
        can_use = check_feature_limit(user_id, feature, count)
        
        # Get current usage and limits
        subscription = get_user_subscription(user_id)
        if subscription:
            current_usage = getattr(subscription, f'{feature}_used', 0)
            limit = getattr(subscription.tier, f'max_{feature}', 0)
            tier_name = subscription.tier.name
        else:
            # Free tier
            free_tier = SubscriptionTier.query.filter_by(name='free').first()
            current_usage = 0
            limit = getattr(free_tier, f'max_{feature}', 0) if free_tier else 0
            tier_name = 'free'
        
        return jsonify({
            'success': True,
            'can_use': can_use,
            'feature': feature,
            'requested_count': count,
            'current_usage': current_usage,
            'limit': limit if limit > 0 else 'unlimited',
            'tier_name': tier_name,
            'remaining': max(0, limit - current_usage) if limit > 0 else 'unlimited',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Failed to check feature limit: {str(e)}")
        return jsonify({
            'error': 'Failed to check feature limit',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@subscription_bp.route('/payments', methods=['GET'])
@cross_origin()
def get_payment_history():
    """
    Get payment history for current user
    """
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User authentication required'}), 401
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Query payments with pagination
        payments_query = Payment.query.filter_by(user_id=user_id).order_by(Payment.created_at.desc())
        payments_paginated = payments_query.paginate(page=page, per_page=per_page, error_out=False)
        
        payments_data = [payment.to_dict() for payment in payments_paginated.items]
        
        # Calculate totals
        total_paid = db.session.query(db.func.sum(Payment.amount)).filter(
            Payment.user_id == user_id,
            Payment.status == 'completed'
        ).scalar() or 0.0
        
        return jsonify({
            'success': True,
            'payments': payments_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': payments_paginated.total,
                'pages': payments_paginated.pages,
                'has_next': payments_paginated.has_next,
                'has_prev': payments_paginated.has_prev
            },
            'summary': {
                'total_paid': total_paid,
                'currency': 'USD',
                'payment_count': payments_paginated.total
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Failed to get payment history: {str(e)}")
        return jsonify({
            'error': 'Failed to get payment history',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@subscription_bp.route('/crypto-payment', methods=['POST'])
@cross_origin()
def process_crypto_payment():
    """
    Process cryptocurrency payment for subscription
    """
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User authentication required'}), 401
        
        data = request.get_json()
        tier_id = data.get('tier_id')
        billing_cycle = data.get('billing_cycle', 'monthly')
        crypto_currency = data.get('crypto_currency')  # ETH, USDC, etc.
        crypto_amount = data.get('crypto_amount')
        transaction_hash = data.get('transaction_hash')
        wallet_address = data.get('wallet_address')
        network = data.get('network', 'ethereum')
        
        if not all([tier_id, crypto_currency, crypto_amount, transaction_hash, wallet_address]):
            return jsonify({'error': 'Missing required payment information'}), 400
        
        # Get target tier
        target_tier = SubscriptionTier.query.get(tier_id)
        if not target_tier:
            return jsonify({'error': 'Invalid subscription tier'}), 400
        
        # Calculate USD amount
        usd_amount = target_tier.price_yearly if billing_cycle == 'yearly' else target_tier.price_monthly
        
        # Create payment record
        payment = Payment(
            user_id=user_id,
            amount=usd_amount,
            currency='USD',
            payment_method='crypto',
            status='pending',  # Will be verified by blockchain monitoring
            crypto_currency=crypto_currency,
            crypto_amount=float(crypto_amount),
            crypto_wallet_address=wallet_address,
            crypto_network=network,
            crypto_transaction_hash=transaction_hash,
            description=f'{target_tier.display_name} subscription ({billing_cycle}) - Crypto payment',
            billing_period_start=datetime.now(),
            billing_period_end=datetime.now() + (timedelta(days=365) if billing_cycle == 'yearly' else timedelta(days=30))
        )
        
        db.session.add(payment)
        db.session.commit()
        
        # Log the crypto payment attempt
        log_feature_usage(
            user_id=user_id,
            feature='payment',
            action='crypto_payment_submitted',
            resource_id=str(payment.id),
            metadata=json.dumps({
                'crypto_currency': crypto_currency,
                'crypto_amount': crypto_amount,
                'transaction_hash': transaction_hash,
                'network': network,
                'tier_name': target_tier.name
            })
        )
        
        logger.info(f"Crypto payment submitted for user {user_id}: {transaction_hash}")
        
        return jsonify({
            'success': True,
            'payment': payment.to_dict(),
            'message': 'Crypto payment submitted for verification',
            'verification_note': 'Payment will be verified on the blockchain and subscription activated automatically',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Crypto payment processing failed: {str(e)}")
        return jsonify({
            'error': 'Crypto payment processing failed',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

# Error handlers for the blueprint
@subscription_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'The requested subscription endpoint does not exist',
        'timestamp': datetime.now().isoformat()
    }), 404

@subscription_bp.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred in subscription service',
        'timestamp': datetime.now().isoformat()
    }), 500

