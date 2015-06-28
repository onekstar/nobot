# encoding:utf-8
class CeleryConfig(object):
    """
    celery 配置
    """
    CELERY_TIMEZONE = 'Asia/Shanghai'
    BROKER_URL = 'redis://localhost:6379/0',
    CELERY_IMPORTS = [
        'tasks.novel',
        'tasks.chapter',
    ]

class FlaskConfig(object):
    """
    Flask app 配置
    """
    DEBUG = True
    SQLALCHEMY_OPTIONS = {'url': 'mysql://root@localhost:3306/nobot?charset=utf8', 'echo': False}
