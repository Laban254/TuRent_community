from app import app

class Config(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = "1234567889"

    DB_NAME = "production-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "example"

    SESSION_COOKIE_SECURE = True
    
app.config['ENV'] = 'production'

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    
    DB_NAME = "development-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "example"

    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True

    DB_NAME = "development-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "example"

    SESSION_COOKIE_SECURE = False