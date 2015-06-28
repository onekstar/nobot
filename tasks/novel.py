# encoding:utf-8
from tasks.celery import app

from dao.novel import NovelDAO

@app.task
def sync(id=None):
    """
    同步小说
    """
    session = app.DBSession()
    novel_dao = NovelDAO(session, app.logger)
    try:
        if not id:
            novel = novel_dao.get_novel_need_sync()
        else:
            novel = novel_dao.get_by_id(id)
        if not novel:
            return False, u'【错误】此小说不存在'
        result = novel_dao.add_chapters(novel, app.current_task)
        return result
    except:
        app.logger.error('novel sync error|%s|' %(id, ), exc_info=1)
        return False, u'【错误】500'
    finally:
        session.close()

@app.task
def sync_chapters_content(id):
    """
    向所有的chapter添加内容
    """
    session = app.DBSession()
    novel_dao = NovelDAO(session, app.logger)
    try:
        novel = novel_dao.get_by_id(id)
        if not novel:
            return False, u'【错误】此小说不存在'
        result = novel_dao.add_chapters_content(novel, app.current_task)
        return result
    except:
        app.logger.error('chapter content sync error|%s|' %(id, ), exc_info=1)
        return False, u'【错误】500'
    finally:
        session.close()
