# encoding:utf-8
from dao.base import BaseDAO
from dao import rollback_on_exception
from models.novel import Novel

class NovelDAO(BaseDAO):
    """
    小说操作
    """

    @rollback_on_exception
    def add(self, name, rule):
        if self.db.query(Novel).filter(Novel.name == name.strip()).first():
            return False, u'重复创建无效'
        novel = Novel(
            name = name,
            rule = rule,
        )
        self.db.add(novel)
        self.db.commit()
        return True, novel
