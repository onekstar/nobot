# encoding:utf-8
from datetime import datetime, timedelta

from dao.base import BaseDAO
from dao import rollback_on_exception

from models.novel import Novel
from models.chapter import Chapter

from lib.parser.tieba.novel import NovelParser 
from lib.parser.tieba.chapter import ChapterParser

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

    @rollback_on_exception
    def add_chapters(self, novel, task=None):
        """
        添加章节列表
        :task: 如果不为None，则为使用异步队列
        """
        if novel.last_sync_time and (novel.last_sync_time > datetime.now() - timedelta(minutes=10)):
            return False, u'【错误】更新过于频繁'

        novel.last_sync_time = datetime.now() 
        self.db.add(novel)
        self.db.commit()

        parser = NovelParser(novel)
        pn = 0
        count = 1000 
        while True:
            try:
                c, chapter_list = parser.execute(pn)
                count = c or count
                for chapter in chapter_list:
                    if self.db.query(Chapter).filter(Chapter.pageid==chapter.pageid).first():
                        continue
                    chapter.novel_id = novel.id
                    self.db.add(chapter)
                self.db.commit()
            except:
                self.logger.error('Add chapters error|%s|%s|' %(novel.id, pn), exc_info=1)
                self.db.rollback()

            pn += 50

            if task:
                task.update_state(state='PROGRESS', meta={'percent': min(pn/float(count), 1.0) * 100})

            if pn > count:
                break

        return True, ''
    
    def get_by_name(self, name):
        """
        根据名称查找novel
        """
        novel = self.db.query(Novel).filter(Novel.name==name).first()
        return novel

    def get_by_id(self, id):
        """
        根据ID查找novel
        """
        novel = self.db.query(Novel).get(id)
        return novel

    @rollback_on_exception
    def add_chapters_content(self, novel, task=None):
        """
        同步章节内容
        """
        rows = self.db.query(Chapter.id).filter(Chapter.novel_id==novel.id).all() #节约内存，只取ID
        if not rows:
            return False, u'没有可用章节'
            
        count = len(rows)
        p_count = 0
        
        for id in [r[0] for r in rows]:
            chapter = self.db.query(Chapter).get(id)
            if not chapter:
                continue
            if chapter.content: #已同步的跳过
                continue
            parser = ChapterParser(chapter)
            try:
                result, chapter = parser.execute()
                if not result:
                    continue
                self.db.add(chapter)
            except:
                self.logger.error('get chapter content error|%s|%s|%s|' %(self.novel.id, chapter.id, chapter.pageid), exc_info=1)

            # 设置进度
            p_count += 1
            if task:
                task.update_state(state='PROGRESS', meta={'percent': min(p_count/float(count), 1.0) * 100})

        self.db.commit()
        return True, ''

    def get_novel_need_sync(self):
        """
        获取一个需要同步的novel
        """
        max_time = datetime.now() - timedelta(minutes=30) 
        novel = self.db.query(Novel).filter(Novel.last_sync_time<max_time).\
            order_by(Novel.last_sync_time, Novel.id.desc()).first()
        return novel

    def get_contents(self, novel):
        """
        为下载获取content
        """
        rows = self.db.query(Chapter.id).filter(Chapter.novel_id==novel.id).all() #节约内存，只取ID
            
        for id in [r[0] for r in rows]:
            chapter = self.db.query(Chapter).get(id)
            yield chapter.content or u'本章内容暂缺'
    
    def get_chapter_list(self, novel_id, page=None, pagesize=None):
        """
        获取章节列表，支持分页
        """
        query = self.db.query(Chapter.id, Chapter.title, Chapter.publish_time, Chapter.pageid).\
            filter(Chapter.novel_id==novel_id)
        count = query.count()

        query = query.order_by(Chapter.publish_time, Chapter.create_time)

        if page:
            offset = (page-1) * pagesize
            query = query.limit(pagesize).offset(offset)

        return count, query.all()
