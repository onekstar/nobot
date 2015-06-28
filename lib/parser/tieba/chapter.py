#coding:utf-8
from bs4 import BeautifulSoup
import requests

class ChapterParser:
    '章节解析器'

    def __init__(self, chapter):
        self.chapter = chapter 

    def execute(self):
        '解析'
        self.html = self._get_html()
        content = self._parse_html()
        if not content:
            return False, '' 
        return True, content
    
    def _get_html(self):
        '获取html'
        url = 'http://tieba.baidu.com/p/' + self.chapter.pageid
        response = requests.get(url)
        return response.text
    
    def _parse_html(self):
        '解析html'
        soup = BeautifulSoup(self.html)
        elements = soup.find_all('div', class_='d_post_content j_d_post_content  clearfix')
        elements = filter(lambda x: len(x.text) > 500, elements)
        contents = []
        for ele in elements:
            for x in ele.children:
                contents.append(unicode(x).replace('<br>', '\n').replace('</br>', ''))
        return '\n'.join(contents)
