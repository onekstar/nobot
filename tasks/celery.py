# encoding:utf-8
'''
Celery 任务配置
'''
from __future__ import absolute_import
from celery import Celery
from config import CeleryConfig

app = Celery('novel')

app.config_from_object(CeleryConfig)
