# encoding:utf-8
from tests.base import BaseTestCase

from tests.dfo import add_db_functions
from tests.dfo.novel import NovelDFO
from tests.dfo.chapter import ChapterDFO

from tasks.novel import sync as sync_task


@add_db_functions(NovelDFO, ChapterDFO)
class NovelViewTestCase(BaseTestCase):
    """
    Novel相关接口测试用例
    """

    def test_add(self):
        """
        测试添加Novel
        """
        params = {
            'name': u'择天记',
            'rule': u'rule'
        }
        result = self.json_post_request('/api/novel/add', params=params)
        self.assertEqual(result['code'], 0)
        self.assertTrue(result['data'])

    def test_sync(self):
        """
        测试发起同步
        """
        novel = self.db_add_novel(name=u'爸爸爸爸吧', rule=u'rule')
        params = {
            'id': novel.id
        }

        result = self.json_post_request('/api/novel/sync', params=params)
        self.assertEqual(result['code'], 0)
        self.assertTrue(result['data']['task_id'])
        self.assertTrue(result['data']['state'])

    def test_sync_content(self):
        """
        测试发起章节内容同步
        """
        novel = self.db_add_novel(name=u'爸爸爸爸吧', rule=u'rule')
        for pageid in ['3857497226', '3855582980', '3848313003']:
            chapter = self.db_add_chapter(
                novel_id=novel.id,
                pageid=unicode(pageid),
                title=u'测试章节%s' %pageid,
            )

        params = {
            'id': novel.id
        }

        result = self.json_post_request('/api/novel/content/sync', params=params)

        self.assertEqual(result['code'], 0)
        self.assertTrue(result['data']['task_id'])
        self.assertTrue(result['data']['state'])

    def test_download(self):
        """
        测试下载章节内容
        """
        novel = self.db_add_novel(name=u'爸爸爸爸吧', rule=u'rule')
        for pageid in ['3857497226', '3855582980', '3848313003']:
            chapter = self.db_add_chapter(
                novel_id=novel.id,
                pageid=unicode(pageid),
                title=u'测试章节%s' %pageid,
                content=u'章节内容%s' %pageid,
            )

        params = {
            'id': novel.id
        }

        response = self.common_request('/api/novel/download', params=params, method='GET')

        self.assertEqual(response.status_code, 200)

    def test_get_chapter_list(self):
        """
        测试获取章节列表
        """
        novel = self.db_add_novel(name=u'择天记', rule=u'^【择天记】.+第.+章.+$')
        for pageid in range(1, 20):
            chapter = self.db_add_chapter(
                novel_id=novel.id,
                pageid=unicode(pageid),
                title=u'测试章节%s' %pageid,
            )

        params = {
            'id': novel.id,
            'page': 1,
            'pagesize': 10
        }
        result = self.json_get_request('/api/novel/chapter/list', params=params)
        self.assertEqual(result['code'], 0)
