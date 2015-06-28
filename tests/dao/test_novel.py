# encoding:utf-8
import requests_mock

from tests.base import BaseTestCase
from tests.dfo import add_db_functions
from tests.dfo.novel import NovelDFO
from tests.dfo.chapter import ChapterDFO

from dao.novel import NovelDAO

@add_db_functions(NovelDFO, ChapterDFO)
class NovelDAOTestCase(BaseTestCase):
    """
    Novel 数据操作测试用例
    """

    def setUp(self):
        super(NovelDAOTestCase, self).setUp()
        self.novel_dao = NovelDAO(self.db, self.app.logger)

    def test_add(self):
        """
        测试添加Novel
        """
        result, novel = self.novel_dao.add(u'测试', u'测试rule')
        self.assertEqual(result, True)
        novel = self.db_get_novel(novel.id)
        for k, v in {'name': u'测试', 'rule': u'测试rule'}.items():
            self.assertEqual(v, getattr(novel, k))

    def test_add_when_exist(self):
        """
        测试添加Novel，当已存在
        """
        novel = self.db_add_novel(name=u'测试', rule=u'')
        result, msg = self.novel_dao.add(u'测试', u'测试rule')
        self.assertFalse(result)
        self.assertEqual(msg, u'重复创建无效')

    @requests_mock.mock()
    def test_add_chapters(self, mock):
        """
        测试生成章节列表
        """
        self._mock_tieba_response(mock, '/f/good', file_path='tests/mock/chapter-list-mock.html')

        novel = self.db_add_novel(name=u'择天记', rule=u'^【择天记】.+第.+章.+$')
        result = self.novel_dao.add_chapters(novel) 
        self.assertTrue(result)
        chapters = self.db_get_chapters_by_novel_id(novel.id)
        self.assertTrue(chapters)

    def test_get_by_name(self):
        """
        测试根据名称查找novel
        """
        novel = self.db_add_novel(name=u'择天记', rule=u'^【择天记】.+第.+章.+$')
        novel = self.novel_dao.get_by_name(novel.name)
        self.assertTrue(novel)

    def test_get_by_id(self):
        """
        测试根据id查找novel
        """
        novel = self.db_add_novel(name=u'择天记', rule=u'^【择天记】.+第.+章.+$')
        novel = self.novel_dao.get_by_id(novel.id)
        self.assertTrue(novel)

    def test_add_chapters_content(self):
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
        result, msg = self.novel_dao.add_chapters_content(novel)
        self.assertTrue(result)
        chapters = self.db_get_chapters_by_novel_id(novel.id)
        for chapter in chapters:
            self.assertTrue(chapter.content)
        

    def test_get_novel_need_sync(self):
        """
        测试获取一个需要同步的novel
        """
        novel = self.db_add_novel(name=u'择天记', rule=u'^【择天记】.+第.+章.+$')
        result = self.novel_dao.get_novel_need_sync()
        self.assertTrue(result)

