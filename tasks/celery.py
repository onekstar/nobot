# encoding:utf-8
'''
Celery 任务配置
'''
from __future__ import absolute_import
import logging

from celery import Celery
from config import CeleryConfig

from sqlalchemy.engine import engine_from_config
from sqlalchemy.orm import sessionmaker, scoped_session

app = Celery('novel')

app.config_from_object(CeleryConfig)


sa_engine = engine_from_config(app.conf['SQLALCHEMY_OPTIONS'], prefix='')
app.DBSession = sessionmaker(bind=sa_engine)

logger = logging.getLogger('nobot.celery')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s]-[%(name)s]-[%(levelname)s]:  %(message)s')
s_handler = logging.StreamHandler()
s_handler.setLevel(logging.WARNING)
s_handler.setFormatter(formatter)
logger.addHandler(s_handler)
app.logger = logger
