# encoding:utf-8
from functools import wraps

def rollback_on_exception(func):
    """
    事务操作装饰器
    """
    @wraps(func)
    def wrapper(dao, *args, **kwargs):
        try:
            result = func(dao, *args, **kwargs)
            return result
        except Exception, e:
            dao.db.rollback()
            dao.logger.error('EXCEPTION IN DAO %s' %func.__name__, exc_info=1)
            return False, u'数据库操作失败'
    return wrapper
