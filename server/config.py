import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    MAIL_SERVER = 'smtp-mail.gmail.com'
    MAIL_DEBUG = 0
    MAIL_USE_TLS = True
    MAIL_PORT = 587
    MAIL_USERNAME = 'arxiv.research@gmail.com'
    MAIL_PASSWORD = 'ArxivResearch1!'
    MAIL_DEFAULT_SENDER = 'arxiv.research@gmail.com'
    MONGO_URI = 'mongodb://mongodb0.example.com:27017'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "models", "data.sqlite")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
