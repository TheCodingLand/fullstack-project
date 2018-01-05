import os

class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
 
class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = False


class TestingConfig(BaseConfig):
    """Testing configuration"""
    DEBUG = False
    TESTING = True


class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False
