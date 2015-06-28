# encoding:utf-8
from tests.base import BaseTestCase

from tests.dfo import add_db_functions
from tests.dfo.novel import NovelDFO
from tests.dfo.chapter import ChapterDFO

@add_db_functions(NovelDFO, ChapterDFO)
class ChapterViewTestCase(BaseTestCase):
    """
    章节接口测试用例
    """

    def test_read_when_novel_id(self):
        """
        测试在线阅读接口，当传入novel id
        """
        novel = self.db_add_novel(name=u'择天记', rule=u'^【择天记】.+第.+章.+$')
        for pageid in range(1, 20):
            chapter = self.db_add_chapter(
                novel_id=novel.id,
                pageid=unicode(pageid),
                title=u'测试章节%s' %pageid,
            )

        params = {
            'novel_id': novel.id,
        }
        result = self.json_get_request('/api/chapter/read', params=params)
        self.assertEqual(result['code'], 0)
