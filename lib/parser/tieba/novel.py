#coding:utf-8
import re
from models.chapter import Chapter
import requests
from bs4 import BeautifulSoup

class NovelParser():
    
    def __init__(self, novel, pn):
        self.novel = novel
        self.pn = pn
        self.rule = re.compile(self.novel.rule)
    
    def execute(self):
        '执行解析'
        self.html = self._get_html()
        if not self.html:
            raise Exception('GET HTML PAGE ERROR|%s|%s' %(self.novel.id, self.novel.name))
        count, chapter_list = self._parse_html()
        if count == 0:
            raise Exception('GET HTML PAGE ERROR|%s|%s' %(self.novel.id, self.novel.name))
        return count, chapter_list
    
    def _get_html(self):
        '获取html内容'
        url = 'http://tieba.baidu.com/f/good'
        params = {
            'kw': self.novel.name,
            'tab': 'good',
            'pn': self.pn,
            'ie': 'utf-8',
        }
        response = requests.get(url, params=params)
        return response.text
    
    def _parse_html(self):
        '解析html, 返回chapter对象列表'
        soup = BeautifulSoup(self.html)
        count_span = soup.find('span', class_='red')
        count = int(count_span.text)

        chapter_list = []
        elements = soup.find_all('a', class_='j_th_tit')
        for ele in elements:
            title = ele.text
            if not self.rule.match(title):
                continue
            url = ele['href']
            pageid = url.strip('/p/')
            chapter = Chapter(
                novel_id=self.novel.id,
                title=title,
                pageid=pageid,
            )
            chapter_list.append(chapter)

        return count, chapter_list 
