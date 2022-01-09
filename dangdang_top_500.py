#!/usr/bin/env python
# encoding: utf-8
'''
#-------------------------------------------------------------------
#                   CONFIDENTIAL --- CUSTOM STUDIOS
#-------------------------------------------------------------------
#
#                   @Project Name : 获取当当网五星好评前五百的书籍
#
#                   @File Name    : dangdang_top_500.py
#
#                   @Programmer   : autofelix
#
#                   @Start Date   : 2022/01/09 13:14
#
#                   @Last Update  : 2022/01/09 13:14
#
#-------------------------------------------------------------------
'''
import re, json, requests

class dangdang:
    '''
     This is a main Class, the file contains all documents.
     One document contains paragraphs that have several sentences
     It loads the original file and converts the original file to new content
     Then the new content will be saved by this class
    '''
    def __init__(self):
        self.url = 'http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-%s'
        self.page = 26

    def hello(self):
        '''
        This is a welcome speech
        :return: self
        '''
        print('*' * 50)
        print(' ' * 10 + '获取当当网五星好评前五百的书籍')
        print(' ' * 5 + '作者: autofelix  Date: 2022-01-09 13:14')
        print(' ' * 5 + '主页: https://autofelix.blog.csdn.net')
        print('*' * 50)
        return self

    def request_dandan(self, url):
        '''
        Send a request
        '''
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
        except requests.RequestException as e:
            print(e)
            return None


    def parse_result(self, html):
        '''
        Parse the result
        '''
        pattern = re.compile(
            '<li.*?list_num.*?(\d+)\.</div>.*?<img src="(.*?)".*?class="name".*?title="(.*?)">.*?class="star">.*?class="tuijian">(.*?)</span>.*?class="publisher_info">.*?target="_blank">(.*?)</a>.*?class="biaosheng">.*?<span>(.*?)</span></div>.*?<p><span class="price_n">(.*?)</span>.*?</li>', re.S)
        items = re.findall(pattern, html)

        for item in items:
            yield {
                'range': item[0],
                'image': item[1],
                'title': item[2],
                'recommend': item[3],
                'author': item[4],
                'times': item[5],
                'price': item[6]
            }

    def write_item_to_file(self, item):
        '''
        Write the file
        '''
        print('开始写入数据 ====> ' + str(item))
        with open('book.txt', 'a', encoding='UTF-8') as f:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')


    def run(self):
        '''
        program entry
        '''
        for i in range(1, self.page):
            html = self.request_dandan(self.url % i)
            items = self.parse_result(html)
            for item in items:
                self.write_item_to_file(item)

if __name__ == '__main__':
    dangdang().hello().run()
