# encoding:utf-8
from datetime import datetime
from sqlalchemy import (Column, Integer, DateTime, SmallInteger, Text, Unicode)

from models.base import BaseModel

class Chapter(BaseModel):
    """
    Chapter 表定义
    """
    __tablename__ = 'chapter'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}
    
    novel_id = Column(Integer, index=True, nullable=False)
    title = Column(Unicode(127), nullable=False, default=u'')
    pageid = Column(Unicode(127), nullable=False, unique=True)
    content = Column(Text, nullable=True)
    status = Column(SmallInteger, nullable=False, default=0)
    publish_time = Column(DateTime, nullable=False, default=datetime.fromtimestamp(0), index=True)
