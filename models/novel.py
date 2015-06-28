# encoding:utf-8
from models.base import BaseModel
from sqlalchemy import (Column, Integer, DateTime, SmallInteger, Unicode)

class Novel(BaseModel):
    """
    novel 表定义
    """
    __tablename__ = 'novel'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}

    name = Column(Unicode(127), nullable=False, index=True, unique=True)
    rule = Column(Unicode(1024), nullable=False, default=u'')
    is_deleted = Column(SmallInteger, default=0) 
    last_sync_time = Column(DateTime, default=0, index=True)
