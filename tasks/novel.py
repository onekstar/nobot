# encoding:utf-8
from tasks.celery import app

@app.task
def hello():
    return 'hello novel'
