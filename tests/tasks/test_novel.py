# encoding:utf-8
import requests_mock

from tests.base import BaseTestCase
from tests.dfo import add_db_functions
from tests.dfo.novel import NovelDFO
from tests.dfo.chapter import ChapterDFO

from tasks import novel as novel_task

@add_db_functions(NovelDFO, ChapterDFO)
class NovelTaskTestCase(BaseTestCase):
    """
    Novel 任务测试用例
    """

    def test_sync_when_novel_not_exist(self):
        """
        测试同步, 当Nove不存在 
        """
        result, msg = novel_task.sync.apply(args=(123, )).get()
        self.assertFalse(result)
        self.assertEqual(msg, u'【错误】此小说不存在')

    @requests_mock.mock()
    def test_sync(self, mock):
        """
        测试同步
        """
        self._mock_tieba_response(mock, '/f/good', file_path='tests/mock/chapter-list-mock.html')

        novel = self.db_add_novel(name=u'择天记', rule=u'^【择天记】.+第.+章.+$')
        result, msg = novel_task.sync.apply(args=(novel.id, )).get()
        self.assertTrue(result)
    
    def test_sync_chapters_content(self):
        """
        测试获取章节内容
        """
        novel = self.db_add_novel(name=u'择天记', rule=u'^【择天记】.+第.+章.+$')
        chapter_list = []
        for pageid in ['3857497226', '3855582980', '3848313003']:
            chapter = self.db_add_chapter(
                novel_id=novel.id,
                pageid=unicode(pageid),
                title=u'测试章节%s' %pageid,
            )
            chapter_list.append(chapter)

        result, msg = novel_task.sync_chapters_content.apply(args=(novel.id, )).get()
        self.assertTrue(result)
        chapters = self.db_get_chapters_by_novel_id(novel.id)
        for chapter in chapters:
            self.assertTrue(chapter.content)

    def test_schedule_sync(self):
        """
        测试定时同步任务
        """
        novel = self.db_add_novel(name=u'abc', rule=u'')
        result, msg = novel_task.sync.apply(args=()).get()
        self.assertTrue(result)
