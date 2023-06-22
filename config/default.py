from datetime import timedelta

class Config(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///production.db"
    SECRET_KEY = "6E27E68DAD3C719FE2B9666D8462D"
    JWT_SECRET_KEY = "6E27E68DAD3C719FE2B9666D8462D"
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=1)
    TEST = False
    DEBUG = False
    CACHE_TYPE = "SimpleCache" # Flask-Caching related configs
    CACHE_DEFAULT_TIMEOUT = 300 # seconds


class ProConfig(Config):
    pass

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"
    SECRET_KEY = "XXX"
    JWT_SECRET_KEY = "XXX"
    
    SECRET_KEY = "dev"
    JWT_SECRET_KEY = "dev"
    TEST = True
    DEBUG = True

class TestConfig(Config):
    TEST = True
    DEBUG = False
    SECRET_KEY = "dev"
    JWT_SECRET_KEY = "dev"

    SQLALCHEMY_DATABASE_URI = "sqlite:///"