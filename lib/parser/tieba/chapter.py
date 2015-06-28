#coding:utf-8
import json
from datetime import datetime
from bs4 import BeautifulSoup
import requests

class ChapterParser:
    '章节解析器'

    def __init__(self, chapter):
        self.chapter = chapter 

    def execute(self):
        '解析'
        self.html = self._get_html()
        self._parse_html()
        if not self.chapter.content:
            raise Exception('Parse chapter content error|%s|%s' %(self.chapter.id, self.chapter.pageid))
        return True, self.chapter 
    
    def _get_html(self):
        '获取html'
        url = 'http://tieba.baidu.com/p/' + self.chapter.pageid
        response = requests.get(url)
        return response.text
    
    def _parse_html(self):
        '解析html'
        soup = BeautifulSoup(self.html)
        self.chapter.content = self._get_content(soup) 
        self.chapter.publish_time = self._get_publish_time(soup) 

    def _get_content(self, soup):
        """
        获取章节内容
        """
        for cla in ['d_post_content j_d_post_content ', 'd_post_content j_d_post_content  clearfix']:
            elements = soup.find_all('div', class_=cla)
            if elements:
                break
        elements = filter(lambda x: len(x.text) > 500, elements)
        contents = []
        for ele in elements:
            for x in ele.children:
                contents.append(unicode(x).replace('<br>', '\n').replace('</br>', ''))
        content = '\n'.join(contents)
        return content

    def _get_publish_time(self, soup):
        """
        获取发布时间
        """
        try:
            for cla in ['l_post l_post_bright j_l_post clearfix', 'l_post l_post_bright noborder']:
                elements = soup.find_all('div', class_=cla)
                if elements:
                    break
            if elements:
                element = elements[0]
                data = json.loads(element['data-field'])
                date = data['content'].get('date') 
            if not date:
                date = soup.find_all('span', class_='tail-info')[1].text
            publish_time = datetime.strptime(date, '%Y-%m-%d %H:%M')
        except:
            publish_time = datetime.fromtimestamp(0)
            print self.chapter.pageid
            import traceback
            traceback.print_exc()
        return publish_time

    

