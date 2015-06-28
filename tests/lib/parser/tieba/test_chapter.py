# encoding:utf-8
from tests.base import BaseTestCase
from tests.dfo import add_db_functions
from tests.dfo.chapter import ChapterDFO
from tests.dfo.novel import NovelDFO

from lib.parser.tieba.chapter import ChapterParser

@add_db_functions(ChapterDFO, NovelDFO)
class ChapterParserTestCase(BaseTestCase):
    """
    章节解析测试用例
    """
    
    def test_execute(self):
        """
        """
        novel = self.db_add_novel(name=u'则添加', rule=u'')
        chapter = self.db_add_chapter(title=u'【择天记】第一卷 第二百四十章 杂物间的大老鼠', pageid=u'3406030297', novel_id=novel.id)
        parser = ChapterParser(chapter)
        result, content = parser.execute()
        self.assertTrue(result)
        self.assertTrue(content)
