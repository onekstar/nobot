# encoding:utf-8
from dao.base import BaseDAO
from models.chapter import Chapter

class ChapterDAO(BaseDAO):
    """
    章节操作
    """

    def read(self, chapter_id, novel_id):
        """
        阅读章节
        """
        if chapter_id:
            chapter = self.db.query(Chapter).filter(Chapter.id==chapter_id).first()
        else:
            chapter = self.db.query(Chapter).filter(Chapter.novel_id==novel_id).\
                order_by(Chapter.pageid).first()
        if not chapter:
            return None, None, None

        pre = self.db.query(Chapter).filter(Chapter.novel_id==chapter.novel_id).\
            filter(Chapter.pageid<chapter.pageid).first()
        if pre:
            pre = pre.id

        next_ = self.db.query(Chapter).filter(Chapter.novel_id==chapter.novel_id).\
            filter(Chapter.pageid>chapter.pageid).first()
        if next_:
            next_ = next_.id

        return pre, chapter, next_



        

