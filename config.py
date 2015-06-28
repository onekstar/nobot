# encoding:utf-8
from datetime import timedelta

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
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

    CELERYBEAT_SCHEDULE = {
        'sync-interval-seconds': {
            'task': 'task.novel.sync',
            'schedule': timedelta(seconds=300),
            'args': ()
        }
    }

class FlaskConfig(object):
    """
    Flask app 配置
    """
    DEBUG = True
    SECRET_KEY = u'j,*()PL<NERTYSD@#$%^'

CeleryConfig.SQLALCHEMY_OPTIONS = FlaskConfig.SQLALCHEMY_OPTIONS = SQLALCHEMY_OPTIONS = {
    'url': 'mysql://root@localhost:3306/nobot?charset=utf8', 'echo': False
}

