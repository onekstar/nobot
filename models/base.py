# encoding:utf-8
from __future__ import unicode_literals, division

from datetime import datetime

from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.schema import MetaData
from sqlalchemy import (Column, Integer, DateTime, SmallInteger)

metadata = MetaData()

@as_declarative(metadata=metadata)
class BaseModel(object):
    """
    base model
    """
    id = Column(Integer, autoincrement=True, primary_key=True)
    create_time = Column(DateTime, index=True, nullable=False, default=datetime.now)
    update_time = Column(DateTime, index=True, nullable=False, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        rst_dict = {}
        for column in self.__table__.columns:
            key = column.name
            value = getattr(self, key)
            if isinstance(value, datetime):
                rst_dict[key] = value.strftime("%Y-%m-%d %H:%M:%S")
            else:
                rst_dict[key] = value
        return rst_dict

    def __repr__(self):
        if not hasattr(self, "id"):
            return object.__repr__(self)
        return "%s(id=%r)" % (type(self).__name__, self.id)
