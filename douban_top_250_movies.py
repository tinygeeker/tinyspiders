#!/usr/bin/env python
# encoding: utf-8
'''
#-------------------------------------------------------------------
#                   CONFIDENTIAL --- CUSTOM STUDIOS
#-------------------------------------------------------------------
#
#                   @Project Name : 豆瓣最受欢迎的250部电影
#
#                   @File Name    : douban_top_250_movies.py
#
#                   @Programmer   : autofelix
#
#                   @Start Date   : 2022/01/10 13:14
#
#                   @Last Update  : 2022/01/10 13:14
#
#-------------------------------------------------------------------
'''
import requests, xlwt
from bs4 import BeautifulSoup

class douban:
    def __init__(self):
        '''
         This is a main Class, the file contains all documents.
         One document contains paragraphs that have several sentences
         It loads the original file and converts the original file to new content
         Then the new content will be saved by this class
        '''
        self.url = 'https://movie.douban.com/top250'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/88.0.4324.146 Safari/537.36',
        }
        self.row = 1

    def hello(self):
        '''
        This is a welcome speech
        :return: self
        '''
        print('*' * 50)
        print(' ' * 15 + '豆瓣最受欢迎的250部电影')
        print(' ' * 5 + '作者: autofelix  Date: 2022-01-10 13:14')
        print(' ' * 5 + '主页: https://autofelix.blog.csdn.net')
        print('*' * 50)
        return self

    def request(self, url):
        '''
        Send a request
        '''
        try:
            response = requests.get(url=url, headers=self.headers)
            if response.status_code == 200:
                return response.text
        except requests.RequestException:
            return None

    def save_to_excel(self, soup):
        '''
        Save info to excel
        '''
        book = xlwt.Workbook(encoding='utf-8', style_compression=0)

        sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)
        sheet.write(0, 0, '名称')
        sheet.write(0, 1, '图片')
        sheet.write(0, 2, '排名')
        sheet.write(0, 3, '评分')
        sheet.write(0, 4, '作者')
        sheet.write(0, 5, '简介')

        list = soup.find(class_='grid_view').find_all('li')

        for item in list:
            item_name = item.find(class_='title').string
            item_img = item.find('a').find('img').get('src')
            item_index = item.find(class_='').string
            item_score = item.find(class_='rating_num').string
            item_author = item.find('p').text
            if item.find(class_='inq') is not None:
                item_intro = item.find(class_='inq').string
            else:
                item_intro = 'NOT AVAILABLE'

            print('爬取电影：' + item_index + ' | ' + item_name + ' | ' + item_score + ' | ' + item_intro)

            sheet.write(self.row, 0, item_name)
            sheet.write(self.row, 1, item_img)
            sheet.write(self.row, 2, item_index)
            sheet.write(self.row, 3, item_score)
            sheet.write(self.row, 4, item_author)
            sheet.write(self.row, 5, item_intro)

            self.row += 1
        book.save(u'豆瓣最受欢迎的250部电影.xlsx')

    def run(self):
        '''
        program entry
        '''
        for i in range(0, 10):
            target_url = self.url + '?start=' + str(i * 25) + '&filter='
            html = self.request(target_url)
            soup = BeautifulSoup(html, 'lxml')
            self.save_to_excel(soup)

if __name__ == '__main__':
    douban().hello().run()
