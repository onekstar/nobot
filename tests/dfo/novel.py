# encoding:utf-8
from tests.dfo.base import BaseDFO

from models.novel import Novel

class NovelDFO(BaseDFO):
    """
    小说操作
    """

    DB_TABLES = ['novel']

    def db_get_novel(self, id):
        """
        获取Novel
        """
        self.db.rollback()
        novel = self.db.query(Novel).get(id)
        return novel
        
    def db_add_novel(self, **kwargs):
        """
        创建novel
        """
        self.db.rollback()
        novel = Novel(**kwargs)
        self.db.add(novel)
        self.db.commit()
        return novel
