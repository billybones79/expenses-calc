import os
class Config(object):
    
    DEBUG = True
    SECRET_KEY = 'L8IsEh26sFUbGj0FL02CUD323mrO8662'
    MONGODB_DATABASE = 'python'
    PROPAGATE_EXCEPTIONS = True
    SECRET_KEY = os.environ.get('SECRET_KEY','\xfb\x13\xdf\xa1@i\xd6>V\xc0\xbf\x8fp\x16#Z\x0b\x81\xeb\x16')
    HOST_NAME = os.environ.get('OPENSHIFT_APP_DNS','localhost')
    APP_NAME = os.environ.get('OPENSHIFT_APP_NAME','flask')
    IP = os.environ.get('OPENSHIFT_PYTHON_IP','127.0.0.1')
    PORT = int(os.environ.get('OPENSHIFT_PYTHON_PORT',5000))


class ProductionConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    MONGODB_USERNAME =os.environ.get('OPENSHIFT_MONGODB_DB_USERNAME')
    MONGODB_PASSWORD=os.environ.get('OPENSHIFT_MONGODB_DB_PASSWORD')
    MONGODB_HOST=os.environ.get('OPENSHIFT_MONGODB_DB_HOST')
    MONGODB_PORT=os.environ.get('OPENSHIFT_MONGODB_DB_PORT')

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
