#coding:utf-8
import re
from models.chapter import Chapter
import requests
from bs4 import BeautifulSoup

class NovelParser():
    
    def __init__(self, novel):
        self.novel = novel
        self.rule = re.compile(self.novel.rule)
    
    def execute(self, pn):
        '执行解析'
        self.html = self._get_html(pn)
        if not self.html:
            raise Exception('GET HTML PAGE ERROR|%s|%s' %(self.novel.id, pn))
        count, chapter_list = self._parse_html()
        return count, chapter_list
    
    def _get_html(self, pn):
        '获取html内容'
        url = 'http://tieba.baidu.com/f/good'
        params = {
            'kw': self.novel.name,
            'tab': 'good',
            'pn': pn,
            'ie': 'utf-8',
        }
        response = requests.get(url, params=params)
        return response.text
    
    def _parse_html(self):
        '解析html, 返回chapter对象列表'
        soup = BeautifulSoup(self.html)

        count_span = soup.find('span', class_='red')
        if not count_span:
            count = 0
        else:
            count = int(count_span.text)

        chapter_list = []
        elements = soup.find_all('a', class_='j_th_tit')
        for ele in elements:
            title = ele.text
            if not self.rule.match(title):
                continue
            url = ele['href']
            pageid = url.strip('/p/').split('?')[0]
            chapter = Chapter(
                novel_id=self.novel.id,
                title=title,
                pageid=pageid,
            )
            chapter_list.append(chapter)

        return count, chapter_list 
