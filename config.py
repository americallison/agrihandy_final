# This script contains configuration settings for the AgriHandy application. 
# Variables used in the configuration settings are stored in the virtual environment.
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev#&.keypo)PoSEC67RET'
    UPLOAD_FOLDER = 'agri_app/static/products_imgs/'
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    #MAIL_SERVER = 'smtp.googlemail.com'
    #MAIL_PORT = 465
    #MAIL_USE_TLS = False
    #MAIL_USE_SSL = True
    #MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'americ474@gmail.com'
    #MAIL_PASSWORD = 'dpabs@45000'
    #AGRIHANDY_MAIL_SUBJECT_PREFIX = 'AGRIHANDY'
    #AGRIHANDY_MAIL_SENDER = 'AgriHandy Admin <americ474@gmail.com>'
    #AGRIHANDY_ADMIN = os.environ.get('AGRIHANDY_ADMIN') or 'americ474@gmail.com'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MSEARCH_INDEX_NAME = 'msearch'
    MSEARCH_PRIMARY_KEY = 'id'
    MSEARCH_ENABLE = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfiguration(Config):
    DEBUG = True 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev_1.db')


class ProductionConfiguration(Config): 
    SQLALCHEMY_DATABASE_URI = "postgresql//postgres:agrihandy*20@localhost/agrihandydata"


# create dictionary for configurations
config = {
    'development': DevelopmentConfiguration,
    'production': ProductionConfiguration,
    'default': DevelopmentConfiguration
}

