import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_compress import Compress
from flask_jwt_extended import JWTManager
from src.config import config
from src.routes.wallet import wallet_bp

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), '../../dist'))

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    CORS(app, origins=app.config.get('CORS_ORIGINS', []), supports_credentials=True)
    JWTManager(app)
    Compress(app)

    app.register_blueprint(wallet_bp, url_prefix='/api/wallets')

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            # This assumes your index.html is in the 'dist' folder at the root
            return send_from_directory(app.static_folder, 'index.html')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
