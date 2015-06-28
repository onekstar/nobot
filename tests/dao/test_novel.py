# encoding:utf-8
from tests.base import BaseTestCase
from tests.dfo import add_db_functions
from tests.dfo.novel import NovelDFO

from dao.novel import NovelDAO

@add_db_functions(NovelDFO)
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

