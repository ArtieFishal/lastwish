import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MONGODB_URI = os.environ.get('MONGODB_URI') or 'mongodb://localhost:27017/lastwish'
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    
    # Email Configuration
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
    FROM_EMAIL = os.environ.get('FROM_EMAIL') or 'noreply@lastwish.com'
    
    # AWS Configuration
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.environ.get('AWS_REGION') or 'us-east-1'
    S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME') or 'lastwish-documents'
    
    # Payment Configuration
    COINPAYMENTS_PUBLIC_KEY = os.environ.get('COINPAYMENTS_PUBLIC_KEY')
    COINPAYMENTS_PRIVATE_KEY = os.environ.get('COINPAYMENTS_PRIVATE_KEY')
    COINPAYMENTS_MERCHANT_ID = os.environ.get('COINPAYMENTS_MERCHANT_ID')
    
    # Blockchain API Keys
    ETHERSCAN_API_KEY = os.environ.get('ETHERSCAN_API_KEY')
    SOLSCAN_API_KEY = os.environ.get('SOLSCAN_API_KEY')
    
    # Security
    ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')
    BCRYPT_LOG_ROUNDS = int(os.environ.get('BCRYPT_LOG_ROUNDS', 12))
    
    # CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:5173').split(',')
    
    # File Upload
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB max file size
    
    # Rate Limiting
    RATELIMIT_STORAGE_URL = "memory://"
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///dev_app.db'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

