# encoding:utf-8
class BaseDAO(object):
    """
    DAO 基类
    """

    def __init__(self, db, logger):
        self.db = db
        self.logger = logger
