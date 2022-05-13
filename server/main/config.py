# project/server/config.py
import os

class BaseConfig:
    """Base configuration."""
    FLASK_APP="main/__init__.py"
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
    DEBUG = False
    CONSUMER_KEY = 'EQWMnC47VbsTBvolrmVlVZJeB'
    CONSUMER_SECRET = 'funxNWwRyCc3rTJWGss6SjJZgMhtVNIeemMyA59h1qqzK2fdGw'
    ACCESS_TOKEN = '1514892570203418625-Vas7CHuYc2X8vJ8vJURNRhnxsHYpId'
    ACCESS_TOKEN_SECRET = 'nMzjFmaiCJyt5S4zv9nQUKFnWSWgJzkgIZaUUyVsQ2FNO'

class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    FLASK_ENV="development"

class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    FLASK_ENV="testing"


class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False
    FLASK_ENV="production"
