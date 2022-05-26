# project/server/config.py
import os

class BaseConfig:
    """Base configuration."""
    FLASK_APP="main/__init__.py"
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
    DEBUG = False
    CONSUMER_KEY = 'AbudTK8RRq04OeUNLarcfrhVG'
    CONSUMER_SECRET = 'ycDmXhzWJwz712Bw3PAlu5PNKyGJgzAuhforfvSe69PY2e23ZR'
    ACCESS_TOKEN = '1125165466446471168-X9pWDuvVuHt9ku9iLGYeu6keSMXamM'
    ACCESS_TOKEN_SECRET = 'iLenhsgAh49JFIZjKSu3Z48LxKwW4C1kIjewpH8xCPZ6k'

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
