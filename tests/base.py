#encoding:utf-8
from __future__ import absolute_import
import copy
import json
from unittest import TestCase
from urllib import urlencode
import requests_mock

from config import FlaskConfig, SQLALCHEMY_OPTIONS 
from sqlalchemy.engine import engine_from_config
from sqlalchemy.orm import scoped_session, sessionmaker

from flask import g, template_rendered

from app import get_wsgi_app
from tasks.celery import app as celery_app

class BaseTestCase(TestCase):
    """
    测试用例基类
    """

    DB_TABLES = []

    def setUp(self, **kwargs):
        super(BaseTestCase, self).setUp()
        SQLALCHEMY_OPTIONS.update({'url': 'mysql://root@localhost:3306/test_nobot?charset=utf8', 'echo': False})
#       SQLALCHEMY_OPTIONS.update({'url': 'mysql://root@localhost:3306/nobot?charset=utf8', 'echo': False})
        self.app = get_wsgi_app(FlaskConfig)
        celery_app.DBSession = sessionmaker(self.app.sa_engine)
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.app.config['TESTING'] = True
        self.app.preprocess_request()
        self.client = self.app.test_client()
        self.login_user_id = 100 
        self.db = self.app.DBSession()
        template_rendered.connect(self._render_callback)
        self.template_context = {}

    def tearDown(self):
        super(BaseTestCase, self).tearDown()
        self.db.rollback()
#       self.DB_TABLES = []
        for table_name in set(self.DB_TABLES):
            self.db.execute('DELETE FROM %s' %table_name)
            self.db.commit()
        self.db.close()
        self.app_context.pop()

    def _render_callback(self, app, template, context):
        """
        保存模板变量
        """
        self.rendered_template = template
        self.template_context = context

    def api_request(self, url, data, login=True):
        headers = {'User-Agent': 'micromessenger', 'Content-Type': 'application/json',}
        if login:
            with self.client.session_transaction() as sess:
                sess['itp_wechat_user_info'] = '123123'
                sess['user_info'] = {'id': self.login_user_id, 'username': 'testaaa'}

        response = self.client.post(url, data=json.dumps(data), headers=headers)
        return response

    def json_post_api_request(self, url, data, login=True):
        response = self.api_request(url, data, login)
        return json.loads(response.data)

    def json_post_request(self, url, params=None, login=True):
        """
        获取Json的post请求
        """
        response = self.common_request(url, params=params, login=login, method='POST')
        return json.loads(response.data)

    def json_get_request(self, url, params=None, login=True):
        """
        获取Json的get请求
        """
        response = self.common_request(url, params=params, login=login, method='GET')
        return json.loads(response.data)

    def common_request(self, url, params=None, login=True, method='POST', headers=None):
        """
        通用的请求
        """
        params = params or {}
        params = copy.copy(params)
        headers = headers or {}
        for k, v in params.items():
            if type(v) is unicode:
                params[k] = v.encode('utf-8')

        headers.update({'User-Agent': 'micromessenger', 'Content-Type': 'application/x-www-form-urlencoded',})
        if login:
            with self.client.session_transaction() as sess:
                sess['itp_wechat_user_info'] = '123123'
                sess['itp_wechat_user_info'] = {'openid': 'open_id_aaaa', 'username': 'testaaa'}
                sess['user_info'] = {'id': self.login_user_id, 'username': 'testaaa', 'avatar': 'people/avatar/default-male.jpg', }

        if method == 'GET':
            url = '%s?%s' %(url, urlencode(params))
            response = self.client.get(url, headers=headers)
        elif method == 'POST':
            response = self.client.post(url, data=urlencode(params), headers=headers)
        return response

    def _mock_tieba_response(self, mock, url, file_path):
        """
        mock 贴吧的请求
        """
        url = 'http://tieba.baidu.com' + url
        text = file(file_path).read().decode('utf-8')
        mock.get(url, status_code=200, text=text)
