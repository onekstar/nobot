# encoding:utf-8
from tests.dfo.base import BaseDFO

from models.chapter import Chapter 

class ChapterDFO(BaseDFO):
    """
    Chapter 操作
    """

    DB_TABLES = ['chapter']

    def db_get_chapter(self, id):
        """
        获取chapter
        """
        self.db.rollback()
        chapter = self.db.query(Chapter).get(id)
        return chapter 

    def db_add_chapter(self, **kwargs):
        """
        添加chapter
        """
        self.db.rollback()
        chapter = Chapter(**kwargs)
        self.db.add(chapter)
        self.db.commit()
        return chapter 

    def db_get_chapters_by_novel_id(self, novel_id):
        """
        根据novel_id 获取 chapter 列表
        """
        self.db.rollback()
        return self.db.query(Chapter).filter(Chapter.novel_id==novel_id).all()
