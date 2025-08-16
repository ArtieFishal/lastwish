import os
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from flask_compress import Compress
from flask_jwt_extended import JWTManager
from datetime import timedelta

# It's better to run the app as a module from the root directory
# e.g., python -m src.main
# The sys.path manipulation has been removed.

from src.config import config

# Import route blueprints
# from src.routes.auth import auth_bp
# from src.routes.user import user_bp
from src.routes.wallet import wallet_bp
# from src.routes.payment import payment_bp
# from src.routes.addendum import addendum_bp
# from src.routes.notification_routes import notification_bp
# from src.routes.legal import legal_bp
# from src.utils.scheduler import init_notification_system

# Import security and performance middleware
# from src.middleware.security import SecurityMiddleware
# from src.utils.performance import init_performance_tools
# from src.utils.encryption import init_encryption_service

def create_app(config_name=None):
    """Application factory pattern with security and performance optimizations"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

    # Load configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Configure CORS
    CORS(app,
         origins=["http://localhost:3000", "http://127.0.0.1:3000"], # Example origins
         supports_credentials=True)

    # Initialize JWT
    jwt = JWTManager(app)

    # Initialize compression
    Compress(app)

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
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    # Register blueprints
    # app.register_blueprint(auth_bp, url_prefix='/api/auth')
    # app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(wallet_bp, url_prefix='/api/wallets')
    # app.register_blueprint(payment_bp, url_prefix='/api/payments')
    # app.register_blueprint(addendum_bp, url_prefix='/api/addendums')
    # app.register_blueprint(notification_bp, url_prefix='/api/notifications')
    # app.register_blueprint(legal_bp, url_prefix='/api/legal')

    # Serve frontend static files
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        static_folder_path = app.static_folder
        if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
            return send_from_directory(static_folder_path, path)
        else:
            index_path = os.path.join(static_folder_path, 'index.html')
            if os.path.exists(index_path):
                return send_from_directory(static_folder_path, 'index.html')
            else:
                return "index.html not found", 404

    @app.route('/api/health')
    def health_check():
        return jsonify({'status': 'healthy'})

    return app

# Create the Flask application
app = create_app()

if __name__ == '__main__':
    # Note: For development, it's often better to use `flask run` command
    # after setting FLASK_APP=src.main
    app.run(host='0.0.0.0', port=5000, debug=True)
