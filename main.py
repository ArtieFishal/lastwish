import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from flask_compress import Compress
from flask_jwt_extended import JWTManager
from datetime import timedelta

from src.config import config
from src.models.user import db
from src.models.payment import SubscriptionPlan, Payment, PaymentWebhook
from src.models.addendum import Addendum, AddendumAsset, AddendumBeneficiary
from src.models.legal_template import LegalTemplate
from src.models.notification import Notification, NotificationTemplate, NotificationPreference, PostDemiseNotification

# Import route blueprints
from src.routes.auth import auth_bp
from src.routes.user import user_bp
from src.routes.wallet import wallet_bp
from src.routes.payment import payment_bp
from src.routes.addendum import addendum_bp
from src.routes.notification_routes import notification_bp
from src.routes.legal import legal_bp
from src.utils.scheduler import init_notification_system

# Import security and performance middleware
from src.middleware.security import SecurityMiddleware
from src.utils.performance import init_performance_tools
from src.utils.encryption import init_encryption_service

def create_app(config_name=None):
    """Application factory pattern with security and performance optimizations"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    
    # Load configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Additional security and performance configuration
    app.config.update(
        # Security settings
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        PERMANENT_SESSION_LIFETIME=timedelta(hours=24),
        
        # Performance settings
        REDIS_URL=os.environ.get('REDIS_URL', 'redis://localhost:6379/0'),
        COMPRESS_MIMETYPES=[
            'text/html',
            'text/css',
            'text/xml',
            'application/json',
            'application/javascript'
        ],
        COMPRESS_LEVEL=6,
        COMPRESS_MIN_SIZE=500,
        
        # Encryption
        ENCRYPTION_MASTER_KEY=os.environ.get('ENCRYPTION_MASTER_KEY', 'master-key-change-in-production'),
        
        # File uploads
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB max file size
        
        # JWT settings
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=24),
        JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=30)
    )
    
    # Initialize extensions
    db.init_app(app)
    
    # Configure CORS with security headers
    CORS(app, 
         origins=app.config['CORS_ORIGINS'], 
         supports_credentials=True,
         allow_headers=['Content-Type', 'Authorization', 'X-CSRF-Token'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Initialize compression
    Compress(app)
    
    # Initialize security middleware
    security_middleware = SecurityMiddleware(app)
    
    # Initialize performance tools
    try:
        cache_manager, performance_monitor = init_performance_tools(app)
    except Exception as e:
        print(f"Warning: Could not initialize performance tools: {e}")
        cache_manager, performance_monitor = None, None
    
    # Initialize encryption service
    try:
        init_encryption_service(app.config['ENCRYPTION_MASTER_KEY'])
    except Exception as e:
        print(f"Warning: Could not initialize encryption service: {e}")
    
    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token has expired'}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'error': 'Invalid token'}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({'error': 'Authorization token is required'}), 401
    
    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request'}), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'error': 'Unauthorized'}), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'error': 'Forbidden'}), 403
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        return jsonify({'error': 'Rate limit exceeded'}), 429
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(wallet_bp, url_prefix='/api/wallets')
    app.register_blueprint(payment_bp, url_prefix='/api/payments')
    app.register_blueprint(addendum_bp, url_prefix='/api/addendums')
    app.register_blueprint(notification_bp, url_prefix='/api/notifications')
    app.register_blueprint(legal_bp, url_prefix='/api/legal')
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Initialize default subscription plans
        initialize_default_data()
        
        # Initialize notification system
        init_notification_system(app)
    
    # Serve frontend static files
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        static_folder_path = app.static_folder
        if static_folder_path is None:
            return "Static folder not configured", 404

        if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
            return send_from_directory(static_folder_path, path)
        else:
            index_path = os.path.join(static_folder_path, 'index.html')
            if os.path.exists(index_path):
                return send_from_directory(static_folder_path, 'index.html')
            else:
                return "index.html not found", 404
    
    # Enhanced health check endpoint
    @app.route('/api/health')
    def health_check():
        """Enhanced health check with performance and security metrics"""
        try:
            # Check database connection
            db.session.execute('SELECT 1')
            
            health_data = {
                'status': 'healthy',
                'version': '1.0.0',
                'database': 'connected'
            }
            
            # Add performance metrics if available
            if performance_monitor:
                health_data['performance'] = performance_monitor.get_performance_stats()
            
            # Add cache stats if available
            if cache_manager:
                health_data['cache'] = cache_manager.get_stats()
            
            return jsonify(health_data)
        except Exception as e:
            return jsonify({
                'status': 'unhealthy',
                'error': str(e)
            }), 500
    
    # Security endpoints
    @app.route('/api/security/csrf-token', methods=['GET'])
    def get_csrf_token():
        """Get CSRF token for forms"""
        from flask import session
        from src.middleware.security import CSRFProtection
        
        CSRFProtection.set_csrf_token()
        return jsonify({'csrf_token': session.get('csrf_token')})
    
    # Performance metrics endpoint
    @app.route('/api/performance/metrics', methods=['GET'])
    def get_performance_metrics():
        """Get performance metrics"""
        if performance_monitor:
            metrics = performance_monitor.get_performance_stats()
            return jsonify(metrics)
        return jsonify({'error': 'Performance monitoring not available'}), 503
    
    return app

def initialize_default_data():
    """Initialize default subscription plans and templates"""
    
    # Check if plans already exist
    if SubscriptionPlan.query.first():
        return
    
    # Create default subscription plans
    plans = [
        {
            'name': 'basic',
            'display_name': 'Basic Plan',
            'price_usd': 49.00,
            'max_wallets': 1,
            'max_beneficiaries': 3,
            'features': [
                'Single wallet connection',
                'Up to 3 beneficiaries',
                'Basic legal templates',
                'PDF generation',
                'Email support'
            ],
            'description': 'Perfect for individuals with a single cryptocurrency wallet'
        },
        {
            'name': 'premium',
            'display_name': 'Premium Plan',
            'price_usd': 149.00,
            'max_wallets': 5,
            'max_beneficiaries': -1,  # Unlimited
            'features': [
                'Up to 5 wallet connections',
                'Unlimited beneficiaries',
                'Advanced legal templates',
                'PDF generation with custom branding',
                'Priority email support',
                'Multi-signature wallet support'
            ],
            'description': 'Ideal for users with multiple wallets and complex estate planning needs'
        },
        {
            'name': 'enterprise',
            'display_name': 'Enterprise Plan',
            'price_usd': 499.00,
            'max_wallets': -1,  # Unlimited
            'max_beneficiaries': -1,  # Unlimited
            'features': [
                'Unlimited wallet connections',
                'Unlimited beneficiaries',
                'Custom legal templates',
                'White-label PDF generation',
                'Dedicated support',
                'Multi-signature wallet support',
                'Advanced tax guidance',
                'Custom integrations'
            ],
            'description': 'Comprehensive solution for high-net-worth individuals and institutions'
        }
    ]
    
    for plan_data in plans:
        plan = SubscriptionPlan(**plan_data)
        db.session.add(plan)
    
    # Create default notification templates
    templates = [
        {
            'name': 'welcome_email',
            'event': 'user_registered',
            'type': 'email',
            'subject_template': 'Welcome to Last Wish - Secure Your Crypto Legacy',
            'content_template': '''Dear {{first_name}},

Welcome to Last Wish! We're honored to help you secure your cryptocurrency legacy for your loved ones.

Your account has been successfully created. Here's what you can do next:

1. Connect your cryptocurrency wallets
2. Assign beneficiaries to your assets
3. Create your notarizable addendum
4. Download your legal documents

If you have any questions, our support team is here to help.

Best regards,
The Last Wish Team''',
            'variables': ['first_name', 'last_name', 'email']
        },
        {
            'name': 'payment_confirmed',
            'event': 'payment_confirmed',
            'type': 'email',
            'subject_template': 'Payment Confirmed - {{plan_name}} Plan Activated',
            'content_template': '''Dear {{first_name}},

Your payment has been confirmed and your {{plan_name}} plan is now active!

Payment Details:
- Plan: {{plan_name}}
- Amount: ${{amount_usd}} USD ({{amount_crypto}} {{cryptocurrency}})
- Transaction: {{transaction_hash}}

You can now access all features of your plan. Start by connecting your wallets and creating your addendum.

Best regards,
The Last Wish Team''',
            'variables': ['first_name', 'plan_name', 'amount_usd', 'amount_crypto', 'cryptocurrency', 'transaction_hash']
        },
        {
            'name': 'addendum_created',
            'event': 'addendum_created',
            'type': 'email',
            'subject_template': 'Your Cryptocurrency Addendum is Ready',
            'content_template': '''Dear {{first_name}},

Your cryptocurrency estate planning addendum has been successfully created and is ready for download.

Addendum Details:
- Title: {{addendum_title}}
- Assets: {{asset_count}} cryptocurrency assets
- Beneficiaries: {{beneficiary_count}} beneficiaries
- Total Value: ${{total_value}} USD

Next Steps:
1. Download your addendum PDF
2. Print and notarize the document
3. Store it with your will or trust
4. Keep credentials separate and secure

Remember: Never include private keys or seed phrases in your addendum.

Best regards,
The Last Wish Team''',
            'variables': ['first_name', 'addendum_title', 'asset_count', 'beneficiary_count', 'total_value']
        }
    ]
    
    for template_data in templates:
        template = NotificationTemplate(**template_data)
        db.session.add(template)
    
    # Create default legal templates
    legal_templates = [
        {
            'name': 'basic_addendum',
            'title': 'Cryptocurrency Estate Planning Addendum',
            'content': '''ADDENDUM TO LAST WILL AND TESTAMENT
CRYPTOCURRENCY AND DIGITAL ASSETS

I, {{full_name}}, being of sound mind and disposing memory, do hereby make this Addendum to my Last Will and Testament dated {{will_date}}, or if no will exists, this document shall serve as a memorandum regarding my cryptocurrency and digital assets.

DIGITAL EXECUTOR
I hereby designate {{digital_executor_name}} ({{digital_executor_email}}) as my Digital Executor to manage my cryptocurrency and digital assets upon my death or incapacity.

CRYPTOCURRENCY ASSETS
The following cryptocurrency assets are held in wallets under my control:

{{asset_list}}

BENEFICIARY DESIGNATIONS
I direct that my cryptocurrency assets be distributed as follows:

{{beneficiary_list}}

DISCOVERY INSTRUCTIONS
{{discovery_instructions}}

IMPORTANT DISCLAIMERS
- This document does NOT contain private keys, seed phrases, or passwords
- Credentials are stored separately in a secure location as indicated above
- Cryptocurrencies are considered property by the IRS and subject to estate tax
- This document is for informational purposes and does not constitute legal advice

Signed this {{date}} day of {{month}}, {{year}}.

_________________________________
{{full_name}}

STATE OF {{state}}
COUNTY OF {{county}}

On this {{date}} day of {{month}}, {{year}}, before me personally appeared {{full_name}}, who proved to me on the basis of satisfactory evidence to be the person whose name is subscribed to the within instrument and acknowledged to me that he/she executed the same in his/her authorized capacity, and that by his/her signature on the instrument the person, or the entity upon behalf of which the person acted, executed the instrument.

I certify under PENALTY OF PERJURY under the laws of the State of {{state}} that the foregoing paragraph is true and correct.

WITNESS my hand and official seal.

_________________________________
Notary Public''',
            'template_type': 'addendum',
            'jurisdiction': 'general',
            'version': '1.0'
        }
    ]
    
    for template_data in legal_templates:
        template = LegalTemplate(**template_data)
        db.session.add(template)
    
    db.session.commit()

# Create the Flask application
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

def initialize_default_data():
    """Initialize default subscription plans and templates"""
    
    # Check if plans already exist
    if SubscriptionPlan.query.first():
        return
    
    # Create default subscription plans
    plans = [
        {
            'name': 'basic',
            'display_name': 'Basic Plan',
            'price_usd': 49.00,
            'max_wallets': 1,
            'max_beneficiaries': 3,
            'features': [
                'Single wallet connection',
                'Up to 3 beneficiaries',
                'Basic legal templates',
                'PDF generation',
                'Email support'
            ],
            'description': 'Perfect for individuals with a single cryptocurrency wallet'
        },
        {
            'name': 'premium',
            'display_name': 'Premium Plan',
            'price_usd': 149.00,
            'max_wallets': 5,
            'max_beneficiaries': -1,  # Unlimited
            'features': [
                'Up to 5 wallet connections',
                'Unlimited beneficiaries',
                'Advanced legal templates',
                'PDF generation with custom branding',
                'Priority email support',
                'Multi-signature wallet support'
            ],
            'description': 'Ideal for users with multiple wallets and complex estate planning needs'
        },
        {
            'name': 'enterprise',
            'display_name': 'Enterprise Plan',
            'price_usd': 499.00,
            'max_wallets': -1,  # Unlimited
            'max_beneficiaries': -1,  # Unlimited
            'features': [
                'Unlimited wallet connections',
                'Unlimited beneficiaries',
                'Custom legal templates',
                'White-label PDF generation',
                'Dedicated support',
                'Multi-signature wallet support',
                'Advanced tax guidance',
                'Custom integrations'
            ],
            'description': 'Comprehensive solution for high-net-worth individuals and institutions'
        }
    ]
    
    for plan_data in plans:
        plan = SubscriptionPlan(**plan_data)
        db.session.add(plan)
    
    # Create default notification templates
    templates = [
        {
            'name': 'welcome_email',
            'event': 'user_registered',
            'type': 'email',
            'subject_template': 'Welcome to Last Wish - Secure Your Crypto Legacy',
            'content_template': '''Dear {{first_name}},

Welcome to Last Wish! We're honored to help you secure your cryptocurrency legacy for your loved ones.

Your account has been successfully created. Here's what you can do next:

1. Connect your cryptocurrency wallets
2. Assign beneficiaries to your assets
3. Create your notarizable addendum
4. Download your legal documents

If you have any questions, our support team is here to help.

Best regards,
The Last Wish Team''',
            'variables': ['first_name', 'last_name', 'email']
        },
        {
            'name': 'payment_confirmed',
            'event': 'payment_confirmed',
            'type': 'email',
            'subject_template': 'Payment Confirmed - {{plan_name}} Plan Activated',
            'content_template': '''Dear {{first_name}},

Your payment has been confirmed and your {{plan_name}} plan is now active!

Payment Details:
- Plan: {{plan_name}}
- Amount: ${{amount_usd}} USD ({{amount_crypto}} {{cryptocurrency}})
- Transaction: {{transaction_hash}}

You can now access all features of your plan. Start by connecting your wallets and creating your addendum.

Best regards,
The Last Wish Team''',
            'variables': ['first_name', 'plan_name', 'amount_usd', 'amount_crypto', 'cryptocurrency', 'transaction_hash']
        },
        {
            'name': 'addendum_created',
            'event': 'addendum_created',
            'type': 'email',
            'subject_template': 'Your Cryptocurrency Addendum is Ready',
            'content_template': '''Dear {{first_name}},

Your cryptocurrency estate planning addendum has been successfully created and is ready for download.

Addendum Details:
- Title: {{addendum_title}}
- Assets: {{asset_count}} cryptocurrency assets
- Beneficiaries: {{beneficiary_count}} beneficiaries
- Total Value: ${{total_value}} USD

Next Steps:
1. Download your addendum PDF
2. Print and notarize the document
3. Store it with your will or trust
4. Keep credentials separate and secure

Remember: Never include private keys or seed phrases in your addendum.

Best regards,
The Last Wish Team''',
            'variables': ['first_name', 'addendum_title', 'asset_count', 'beneficiary_count', 'total_value']
        }
    ]
    
    for template_data in templates:
        template = NotificationTemplate(**template_data)
        db.session.add(template)
    
    # Create default legal templates
    legal_templates = [
        {
            'name': 'basic_addendum',
            'title': 'Cryptocurrency Estate Planning Addendum',
            'content': '''ADDENDUM TO LAST WILL AND TESTAMENT
CRYPTOCURRENCY AND DIGITAL ASSETS

I, {{full_name}}, being of sound mind and disposing memory, do hereby make this Addendum to my Last Will and Testament dated {{will_date}}, or if no will exists, this document shall serve as a memorandum regarding my cryptocurrency and digital assets.

DIGITAL EXECUTOR
I hereby designate {{digital_executor_name}} ({{digital_executor_email}}) as my Digital Executor to manage my cryptocurrency and digital assets upon my death or incapacity.

CRYPTOCURRENCY ASSETS
The following cryptocurrency assets are held in wallets under my control:

{{asset_list}}

BENEFICIARY DESIGNATIONS
I direct that my cryptocurrency assets be distributed as follows:

{{beneficiary_list}}

DISCOVERY INSTRUCTIONS
{{discovery_instructions}}

IMPORTANT DISCLAIMERS
- This document does NOT contain private keys, seed phrases, or passwords
- Credentials are stored separately in a secure location as indicated above
- Cryptocurrencies are considered property by the IRS and subject to estate tax
- This document is for informational purposes and does not constitute legal advice

Signed this {{date}} day of {{month}}, {{year}}.

_________________________________
{{full_name}}

STATE OF {{state}}
COUNTY OF {{county}}

On this {{date}} day of {{month}}, {{year}}, before me personally appeared {{full_name}}, who proved to me on the basis of satisfactory evidence to be the person whose name is subscribed to the within instrument and acknowledged to me that he/she executed the same in his/her authorized capacity, and that by his/her signature on the instrument the person, or the entity upon behalf of which the person acted, executed the instrument.

I certify under PENALTY OF PERJURY under the laws of the State of {{state}} that the foregoing paragraph is true and correct.

WITNESS my hand and official seal.

_________________________________
Notary Public''',
            'template_type': 'addendum',
            'jurisdiction': 'general',
            'version': '1.0'
        }
    ]
    
    for template_data in legal_templates:
        template = LegalTemplate(**template_data)
        db.session.add(template)
    
    db.session.commit()

# Create the Flask application
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
