# Flask Config File
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

class Config(object):

    # main config
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # mail settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # MAIL_USE_SSL = True

    # mail authentication
    MAIL_USERNAME = os.environ['EMAIL_USER']
    MAIL_PASSWORD = os.environ['EMAIL_PASS']

    # Flask Admin theme
    FLASK_ADMIN_SWATCH = 'sandstone'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///chowforex.db'
    SECRET_KEY = '\x9f\xbc\xacOC\x8dr\xb9\x03fj\xfa*\xa07)'

# class TestingConfig(Config):
#     pass
