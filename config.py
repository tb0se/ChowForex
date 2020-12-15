# Flask Config File
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///chowforex.db'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app/chowforex.db')
    SECRET_KEY = '\x9f\xbc\xacOC\x8dr\xb9\x03fj\xfa*\xa07)'

# class TestingConfig(Config):
#     pass
