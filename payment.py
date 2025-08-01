from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
import requests
import hashlib
import hmac

from src.routes.auth import require_auth
from src.models.payment import SubscriptionPlan, Payment, PaymentWebhook
from src.models.user import db
from src.services.email_service import EmailService

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/plans', methods=['GET'])
def get_subscription_plans():
    """Get available subscription plans"""
    try:
        plans = SubscriptionPlan.query.filter_by(is_active=True).all()
        return jsonify({
            'plans': [plan.to_dict() for plan in plans]
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Get plans error: {str(e)}")
        return jsonify({'error': 'Failed to get subscription plans'}), 500

@payment_bp.route('/create', methods=['POST'])
@require_auth
def create_payment():
    """Create a new payment"""
    try:
        user = request.current_user
        data = request.get_json()
        
        plan_id = data.get('plan_id')
        cryptocurrency = data.get('cryptocurrency', 'BTC').upper()
        
        if not plan_id:
            return jsonify({'error': 'Plan ID required'}), 400
        
        # Validate plan
        plan = SubscriptionPlan.query.get(plan_id)
        if not plan or not plan.is_active:
            return jsonify({'error': 'Invalid subscription plan'}), 404
        
        # Validate cryptocurrency
        supported_cryptos = ['BTC', 'ETH', 'USDC', 'SOL', 'LTC']
        if cryptocurrency not in supported_cryptos:
            return jsonify({'error': f'Cryptocurrency not supported. Supported: {supported_cryptos}'}), 400
        
        # Get current exchange rate
        exchange_rate = get_crypto_exchange_rate(cryptocurrency)
        if not exchange_rate:
            return jsonify({'error': 'Unable to get exchange rate'}), 500
        
        amount_crypto = float(plan.price_usd) / exchange_rate
        
        # Create payment record
        payment = Payment(
            user_id=user.id,
            plan_id=plan.id,
            amount_usd=plan.price_usd,
            amount_crypto=amount_crypto,
            cryptocurrency=cryptocurrency,
            exchange_rate=exchange_rate,
            payment_address='',  # Will be set by payment provider
            payment_provider='coinpayments',
            status='pending',
            expires_at=datetime.utcnow() + timedelta(hours=1)  # 1 hour to complete payment
        )
        
        db.session.add(payment)
        db.session.flush()  # Get the payment ID
        
        # Create payment with CoinPayments (mock implementation)
        payment_data = create_coinpayments_payment(payment)
        
        if payment_data:
            payment.payment_address = payment_data.get('address')
            payment.provider_payment_id = payment_data.get('txn_id')
            db.session.commit()
            
            return jsonify({
                'payment': payment.to_dict(),
                'payment_address': payment.payment_address,
                'amount_crypto': amount_crypto,
                'exchange_rate': exchange_rate,
                'expires_at': payment.expires_at.isoformat()
            }), 201
        else:
            db.session.rollback()
            return jsonify({'error': 'Failed to create payment'}), 500
            
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Create payment error: {str(e)}")
        return jsonify({'error': 'Failed to create payment'}), 500

@payment_bp.route('/<int:payment_id>/status', methods=['GET'])
@require_auth
def get_payment_status(payment_id):
    """Get payment status"""
    try:
        user = request.current_user
        payment = Payment.query.filter_by(id=payment_id, user_id=user.id).first()
        
        if not payment:
            return jsonify({'error': 'Payment not found'}), 404
        
        # Check if payment has expired
        if payment.is_expired() and payment.status == 'pending':
            payment.status = 'expired'
            db.session.commit()
        
        return jsonify({'payment': payment.to_dict()}), 200
        
    except Exception as e:
        current_app.logger.error(f"Get payment status error: {str(e)}")
        return jsonify({'error': 'Failed to get payment status'}), 500

@payment_bp.route('/<int:payment_id>/refund', methods=['POST'])
@require_auth
def request_refund(payment_id):
    """Request payment refund"""
    try:
        user = request.current_user
        payment = Payment.query.filter_by(id=payment_id, user_id=user.id).first()
        
        if not payment:
            return jsonify({'error': 'Payment not found'}), 404
        
        if not payment.can_refund():
            return jsonify({'error': 'Payment cannot be refunded'}), 400
        
        data = request.get_json()
        refund_reason = data.get('reason', '').strip()
        
        if not refund_reason:
            return jsonify({'error': 'Refund reason required'}), 400
        
        # Process refund request
        payment.refund_requested_at = datetime.utcnow()
        payment.refund_reason = refund_reason
        payment.status = 'refund_requested'
        
        db.session.commit()
        
        # In production, this would trigger the actual refund process
        # For now, we'll just mark it as requested
        
        return jsonify({
            'message': 'Refund requested successfully',
            'payment': payment.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Refund request error: {str(e)}")
        return jsonify({'error': 'Failed to request refund'}), 500

@payment_bp.route('/history', methods=['GET'])
@require_auth
def get_payment_history():
    """Get user's payment history"""
    try:
        user = request.current_user
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        payments = Payment.query.filter_by(user_id=user.id)\
                                .order_by(Payment.created_at.desc())\
                                .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'payments': [payment.to_dict() for payment in payments.items],
            'total': payments.total,
            'pages': payments.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Get payment history error: {str(e)}")
        return jsonify({'error': 'Failed to get payment history'}), 500

@payment_bp.route('/webhook/coinpayments', methods=['POST'])
def coinpayments_webhook():
    """Handle CoinPayments webhook"""
    try:
        # Verify webhook signature
        if not verify_coinpayments_webhook(request):
            return jsonify({'error': 'Invalid webhook signature'}), 401
        
        data = request.form.to_dict()
        
        # Log webhook
        webhook = PaymentWebhook(
            provider='coinpayments',
            webhook_data=data,
            processed=False
        )
        db.session.add(webhook)
        db.session.commit()
        
        # Process webhook
        process_coinpayments_webhook(webhook, data)
        
        return jsonify({'status': 'ok'}), 200
        
    except Exception as e:
        current_app.logger.error(f"CoinPayments webhook error: {str(e)}")
        return jsonify({'error': 'Webhook processing failed'}), 500

@payment_bp.route('/exchange-rates', methods=['GET'])
def get_exchange_rates():
    """Get current cryptocurrency exchange rates"""
    try:
        cryptocurrencies = ['bitcoin', 'ethereum', 'usd-coin', 'solana', 'litecoin']
        rates = {}
        
        for crypto in cryptocurrencies:
            rate = get_crypto_exchange_rate_by_id(crypto)
            if rate:
                symbol = {
                    'bitcoin': 'BTC',
                    'ethereum': 'ETH',
                    'usd-coin': 'USDC',
                    'solana': 'SOL',
                    'litecoin': 'LTC'
                }.get(crypto, crypto.upper())
                rates[symbol] = rate
        
        return jsonify({'rates': rates}), 200
        
    except Exception as e:
        current_app.logger.error(f"Get exchange rates error: {str(e)}")
        return jsonify({'error': 'Failed to get exchange rates'}), 500

def get_crypto_exchange_rate(symbol):
    """Get cryptocurrency exchange rate from CoinGecko"""
    try:
        coin_ids = {
            'BTC': 'bitcoin',
            'ETH': 'ethereum',
            'USDC': 'usd-coin',
            'SOL': 'solana',
            'LTC': 'litecoin'
        }
        
        coin_id = coin_ids.get(symbol)
        if not coin_id:
            return None
        
        return get_crypto_exchange_rate_by_id(coin_id)
        
    except Exception as e:
        current_app.logger.error(f"Exchange rate fetch error for {symbol}: {str(e)}")
        return None

def get_crypto_exchange_rate_by_id(coin_id):
    """Get exchange rate by CoinGecko coin ID"""
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': coin_id,
            'vs_currencies': 'usd'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        return data.get(coin_id, {}).get('usd')
        
    except Exception as e:
        current_app.logger.error(f"Exchange rate API error for {coin_id}: {str(e)}")
        return None

def create_coinpayments_payment(payment):
    """Create payment with CoinPayments API (mock implementation)"""
    try:
        # This is a mock implementation
        # In production, you would use the actual CoinPayments API
        
        # Mock payment address generation
        mock_addresses = {
            'BTC': '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
            'ETH': '0x742d35Cc6634C0532925a3b8D0C9e3e8d4C4c4c4',
            'USDC': '0x742d35Cc6634C0532925a3b8D0C9e3e8d4C4c4c4',
            'SOL': '11111111111111111111111111111112',
            'LTC': 'LTC1234567890abcdef1234567890abcdef'
        }
        
        return {
            'address': mock_addresses.get(payment.cryptocurrency),
            'txn_id': f"CPAY{payment.id}{payment.cryptocurrency}",
            'status': 'pending'
        }
        
    except Exception as e:
        current_app.logger.error(f"CoinPayments payment creation error: {str(e)}")
        return None

def verify_coinpayments_webhook(request):
    """Verify CoinPayments webhook signature"""
    try:
        # This would verify the HMAC signature from CoinPayments
        # For now, return True (mock implementation)
        return True
        
    except Exception as e:
        current_app.logger.error(f"Webhook verification error: {str(e)}")
        return False

def process_coinpayments_webhook(webhook, data):
    """Process CoinPayments webhook data"""
    try:
        txn_id = data.get('txn_id')
        status = data.get('status')
        
        if not txn_id:
            return
        
        # Find payment by provider payment ID
        payment = Payment.query.filter_by(provider_payment_id=txn_id).first()
        if not payment:
            return
        
        # Update payment status based on webhook
        if status == '100':  # Payment complete
            payment.status = 'confirmed'
            payment.confirmed_at = datetime.utcnow()
            payment.transaction_hash = data.get('payment_address')  # Mock
            
            # Send confirmation email
            try:
                email_service = EmailService()
                email_service.send_payment_confirmation_email(payment.user, payment)
            except Exception as e:
                current_app.logger.error(f"Failed to send payment confirmation email: {str(e)}")
                
        elif status in ['-1', '-2']:  # Payment failed/cancelled
            payment.status = 'failed'
        
        webhook.payment_id = payment.id
        webhook.processed = True
        webhook.processed_at = datetime.utcnow()
        
        db.session.commit()
        
    except Exception as e:
        current_app.logger.error(f"Webhook processing error: {str(e)}")
        webhook.processed = True
        webhook.error_message = str(e)
        db.session.commit()

