class Config(object):
    DEBUG = False
    SECRET_KEY = 'L8IsEh26sFUbGj0FL02CUD323mrO8662'
    MONGODB_DATABASE = 'expenses'


class ProductionConfig(Config):
    DEBUG = False
    MONGODB_USERNAME ='admin'
    MONGODB_PASSWORD="8zse_y19PsLb"


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True