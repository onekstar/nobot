# encoding:utf-8
from tests.base import BaseTestCase
from tests.dfo import add_db_functions
from tests.dfo.novel import NovelDFO
from tests.dfo.chapter import ChapterDFO

from lib.parser.tieba.novel import NovelParser

@add_db_functions(NovelDFO, ChapterDFO)
class NovelParserTestCase(BaseTestCase):
    """
    小说章节解析测试用例
    """

    def test_execute(self):
        """
        测试execute
        """
        novel = self.db_add_novel(name=u'择天记', rule=u'^【择天记】.+第.+章.+$')
        parser = NovelParser(novel)
        count, chapter_list = parser.execute(0)
        self.assertTrue(count)
        self.assertTrue(chapter_list)

    def test_execute_when_pn(self):
        """
        测试execute, 当pn 非0
        """
        novel = self.db_add_novel(name=u'择天记', rule=u'^【择天记】.+第.+章.+$')
        parser = NovelParser(novel)
        count, chapter_list = parser.execute(100)
        self.assertTrue(count)
        self.assertTrue(chapter_list)
