# encoding:utf-8
from tests.base import BaseTestCase
from tasks.novel import sync as sync_task

class TaskViewTestCase(BaseTestCase):

    def test_get_state(self):
        """
        测试获取任务状态
        """
        task = sync_task.apply_async((1, ))
        params = {
            'id': task.id
        }
        result = self.json_get_request('/api/task/state', params=params)
        self.assertEqual(result['code'], 0)
        self.assertTrue(result['data']) 
