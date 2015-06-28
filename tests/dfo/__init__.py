# encoding:utf-8
def add_db_functions(*args):
    """
    为测试用例添加数据库操作功能
    """
    def wrapper(testcase):
        for dfo_class in args:
            for k, v in dfo_class.__dict__.items():
                if k.startswith('db_'):
                    setattr(testcase, k, v)
            testcase.DB_TABLES.extend(dfo_class.DB_TABLES)
        return testcase
    return wrapper
