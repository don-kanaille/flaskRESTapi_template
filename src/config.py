from datetime import timedelta
from os import environ


class Config(object):
    """
    Default configuration.
    """
    ENV = 'production'
    DEBUG = False
    TESTING = False
    SECRET_KEY = "B\xb2?.\xdf\x9f\xa7m\xf8\x8a%,\xf7\xc4\xfa\x91"

    DB_NAME = "production-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "admin"

    SESSION_COOKIE_SECURE = True

    FLASK_SERVER_NAME = 'localhost:5000'
    FLASK_THREADED = True

    JWT_AUTH_URL_RULE = '/login'
    JWT_EXPIRATION_DELTA = timedelta(seconds=1800)

    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL', 'sqlite:///' + DB_NAME + '.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True


class ProductionConfig(Config):
    """
    Production configuration.
    """
    pass


class DevelopmentConfig(Config):
    """
    Development configuration.
    """
    ENV = 'development'
    DEBUG = True

    DB_NAME = "development-db"
    DB_USERNAME = "userjw"
    DB_PASSWORD = "1q2w3e4r"

    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL', 'sqlite:///' + DB_NAME + '.db')

    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    """
    Testing configuration.
    """
    ENV = 'testing'
    TESTING = True

    DB_NAME = "testing-db"
    DB_USERNAME = "userjw"
    DB_PASSWORD = "1q2w3e4r"

    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL', 'sqlite:///' + DB_NAME + '.db')

    SESSION_COOKIE_SECURE = False