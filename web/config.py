"""
Configuration management for Zenthral AI Platform
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""

    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24).hex()

    # Database
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///zenthral.db'
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.environ.get('SQL_DEBUG', 'false').lower() == 'true'

    # JWT
    JWT_SECRET = os.environ.get('JWT_SECRET') or os.urandom(32).hex()
    JWT_ACCESS_TOKEN_EXPIRES = 900  # 15 minutes
    JWT_REFRESH_TOKEN_EXPIRES = 2592000  # 30 days

    # Encryption
    ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY') or os.urandom(32).hex()

    # Email (SendGrid or SMTP)
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
    SMTP_HOST = os.environ.get('SMTP_HOST', 'smtp.sendgrid.net')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
    SMTP_USER = os.environ.get('SMTP_USER')
    SMTP_PASS = os.environ.get('SMTP_PASS')
    FROM_EMAIL = os.environ.get('FROM_EMAIL', 'noreply@zenthral.ai')

    # Gmail OAuth (existing)
    GMAIL_CLIENT_ID = os.environ.get('GMAIL_CLIENT_ID', '175580175862-3au3aea8mr8nll6psp9g705bt3270dr4.apps.googleusercontent.com')
    GMAIL_CLIENT_SECRET = os.environ.get('GMAIL_CLIENT_SECRET', '')
    GMAIL_REDIRECT_URI = 'http://localhost:5001/auth/gmail/callback'

    # AI Providers
    ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

    # Stripe (for later phases)
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
    STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')

    # Application
    APP_NAME = 'Zenthral AI Platform'
    APP_URL = os.environ.get('APP_URL', 'http://localhost:5001')

    # Security
    BCRYPT_LOG_ROUNDS = 12
    PASSWORD_MIN_LENGTH = 8


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    # Use PostgreSQL in production
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    BCRYPT_LOG_ROUNDS = 4  # Faster tests


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Get configuration based on environment"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])
