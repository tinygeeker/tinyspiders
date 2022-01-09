#!/usr/bin/env python
# encoding: utf-8
'''
#-------------------------------------------------------------------
#                   CONFIDENTIAL --- CUSTOM STUDIOS
#-------------------------------------------------------------------
#
#                   @Project Name : 美女图片下载
#
#                   @File Name    : main.py
#
#                   @Programmer   : autofelix
#
#                   @Start Date   : 2022/01/09 13:14
#
#                   @Last Update  : 2022/01/09 13:14
#
#-------------------------------------------------------------------
'''
import concurrent, os, requests
from retrying import retry
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

class xiuren:
    '''
     This is a main Class, the file contains all documents.
     One document contains paragraphs that have several sentences
     It loads the original file and converts the original file to new content
     Then the new content will be saved by this class
    '''
    def __init__(self):
        self.spider_url = 'https://www.tutu555.net/a/cn/xiuren'
        self.total_page = 151

    def hello(self):
        '''
        This is a welcome speech
        :return: self
        '''
        print('*' * 50)
        print(' ' * 20 + '美女图片下载')
        print(' ' * 5 + 'Author: autofelix  Date: 2022-01-09 13:14')
        print('*' * 50)
        return self

    def run(self):
        '''
        program entry
        '''
        list_page_urls = self.get_spider_info()
        with concurrent.futures.ProcessPoolExecutor(max_workers=5) as exector:
            for url in list_page_urls:
                exector.submit(self.download, url)

    @retry(stop_max_attempt_number=3)
    def request(self, url):
        '''
        Send a request
        :param url: the url of request
        :return: the text of request
        '''
        response = requests.get(url, timeout=10)
        assert response.status_code == 200
        response.encoding = 'gbk'
        return response.text


    def get_spider_info(self):
        '''
        Get the info of spider
        :return: list
        '''
        info = []
        for i in range(1, self.total_page):
            print('正在采集第{}页的数据...' . format(i))
            url = '{}/list_6_{}.html'.format(self.spider_url, i)
            spider_html = self.request(url)
            soup = BeautifulSoup(spider_html, 'lxml')
            elements = soup.find(class_='clearfix').find_all('li')
            for item in elements:
                url = item.find('a').get('href')
                title = item.find('a').find('span').string
                info.append('{}__@@__{}' . format(title, url))
        return info

    def download_picture(self, title, image_list):
        '''
        Download picture
        '''
        os.mkdir(title)
        j = 1
        for item in image_list:
            filename = '%s/%s.jpg' % (title, str(j))
            print('正在下载｜%s : NO.%s' % (title, str(j)))
            with open(filename, 'wb') as f:
                img = requests.get(item).content
                f.write(img)
            j += 1

    def download(self, info):
        '''
        Get the info of images
        :return: list
        '''
        url_str = info.split('__@@__')
        title = url_str[0]
        url = url_str[-1]
        spider_html = self.request(url)
        soup = BeautifulSoup(spider_html, 'lxml')
        total = soup.find(class_='page').find_all('a')[-2].string
        image_list = []
        for i in range(int(total)):
            page = i + 1
            page_url = f'_{page}.html'.join(url.split('.html')) if page > 1 else url
            html = self.request(page_url)
            soup = BeautifulSoup(html, 'lxml')
            img_url = soup.find(class_='content').find_all('img')
            for item in img_url:
                im_url = item.get('src')
                image_list.append(im_url)
        self.download_picture(title, image_list)


if __name__ == '__main__':
    xiuren().hello().run()