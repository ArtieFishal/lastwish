import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-secret-key'
    MONGODB_URI = os.environ.get('MONGODB_URI') or 'mongodb://172.17.0.1:27017/lastwish'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'another-very-secret-key'
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:5173').split(',')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
