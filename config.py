class Config(object):
    DEBUG = False
    SECRET_KEY = 'L8IsEh26sFUbGj0FL02CUD323mrO8662'
    MONGODB_DATABASE = 'python'


class ProductionConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    MONGODB_USERNAME =os.environ['OPENSHIFT_MONGODB_DB_USERNAME']
    MONGODB_PASSWORD=os.environ['OPENSHIFT_MONGODB_DB_PASSWORD']
    MONGODB_HOST=os.environ['OPENSHIFT_MONGODB_DB_HOST']
    MONGODB_PORT=os.environ['OPENSHIFT_MONGODB_DB_PORT']
    


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
