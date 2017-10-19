import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '2976626104@qq.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'ciquycpdtlyzdgfi'

    IDACHENGZI_MAIL_SUBJECT_PREFIX = '[Idachengzi]'
    IDACHENGZI_MAIL_SENDER = 'Idachengzi Admin <2976626104@qq.com>'

    IDACHENGZI_ADMIN = os.environ.get('IDACHENGZI_ADMIN') or '2976626104@qq.com'

    IDACHENGZI_POSTS_PER_PAGE=10

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('IDACHENGZI_DATABASE_URL') or 'mysql://root:5547@127.0.0.1/blog_idachengzi'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('IDACHENGZI_DATABASE_URL') or 'mysql://root:5547@127.0.0.1/blog_idachengzi'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('IDACHENGZI_DATABASE_URL') or 'mysql://root:5547@127.0.0.1/blog_idachengzi'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
