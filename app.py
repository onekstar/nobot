# encoding:utf-8
"""
nobot API
"""
import os

import logging
import logging.handlers

from redis import StrictRedis

from flask import Flask, g, _app_ctx_stack, current_app, request

from sqlalchemy.engine import engine_from_config
from sqlalchemy.orm import sessionmaker, scoped_session

from views.novel import bp_novel
from views.task import bp_task
from views.chapter import bp_chapter
from views.index import bp_index


def _logger_init(logger_name, logger_path, logger_level, debug=False):
    """
    日志初始化
    """
    formatter = logging.Formatter('[%(asctime)s]-[%(name)s]-[%(levelname)s]:  %(message)s')
    logger = logging.getLogger(logger_name)
    logger.setLevel(logger_level)

    handler = logging.handlers.TimedRotatingFileHandler(logger_path, when='midnight', interval=1, backupCount=0)
    handler.suffix = '%Y%m%d'
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    if debug:
        s_handler = logging.StreamHandler()
        s_handler.setLevel(logging.WARNING)
        s_handler.setFormatter(formatter)
        logger.addHandler(s_handler)
    return logger

def get_wsgi_app(config):
    
    app = Flask('nobot')
    app.config.from_object(config)

    app.sa_engine = engine_from_config(app.config['SQLALCHEMY_OPTIONS'], prefix='')
    app.DBSession = scoped_session(sessionmaker(bind=app.sa_engine),
                                   scopefunc=_app_ctx_stack.__ident_func__)

    blueprints = [bp_novel, bp_task, bp_chapter, bp_index]
    for bp in blueprints:
        app.register_blueprint(bp)

    @app.before_request
    def before_request():
        if request.endpoint == "static":
            return
        g.db = current_app.DBSession()

    @app.teardown_request
    def teardown_request(exception):
        if request.endpoint == "static":
            return

        g.db.close()
    
    return app

if __name__ == '__main__':
    from config import FlaskConfig
    app = get_wsgi_app(FlaskConfig)
    app.run()
