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
#                   @Programmer   : tinygeeker
#
#                   @Start Date   : 2022/02/22 13:14
#
#                   @Last Update  : 2022/02/22 13:14
#
#-------------------------------------------------------------------
'''
import threading, requests, os
from tqdm import tqdm
from retrying import retry
from bs4 import BeautifulSoup

class ku:
    def __init__(self):
        self.dir_name = 'MiStar魅妍社'
        self.start_page = 1
        self.total_page = 15
        self.url = 'https://www.ku137.net/b/57/list_57_{}.html'
        self.picture_detail_url = []

    def hello(self):
        '''
        This is a welcome speech
        :return: self
        '''
        print('*' * 50)
        print(' ' * 20 + '美女图片下载')
        print(' ' * 5 + '作者: tinygeeker  Date: 2022-02-22 13:14')
        print(' ' * 5 + '主页: https://tinygeeker.blog.csdn.net')
        print('*' * 50)
        return self

    def get_picture_url_list(self):
        picture_url_list = []
        for i in range(self.start_page, self.total_page):
            picture_url = self.url.format(i)
            picture_url_list.append(picture_url)
        return picture_url_list

    def get_picture_detail_list(self):
        picture_url_list = self.get_picture_url_list()
        print('正在采集图片详情...')
        for url in tqdm(picture_url_list):
            spider_html = self.request(url)
            soup = BeautifulSoup(spider_html, 'lxml')
            elements = soup.find(class_='m-list').find_all('li')
            for item in elements:
                url = item.find('a').get('href')
                title = item.find('a').get('title')
                self.picture_detail_url.append('{}__@@__{}'.format(title, url))

    def download(self, info):
        url_str = info.split('__@@__')
        # title = url_str[0]
        title = ''
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
                title = item.get('alt')
                im_url = item.get('src')
                image_list.append(im_url)
        self.download_picture(title, image_list)

    def download_picture(self, title, image_list):
        '''
        Download picture
        '''
        if not os.path.exists(self.dir_name + '/' + title):
            os.mkdir(self.dir_name + '/' + title)

        j = 1
        for item in image_list:
            print('正在下载{}-{}张:'.format(title, str(j)), '▋' * (j // 2))
            filename = '%s/%s/%s.jpg' % (self.dir_name, title, str(j))
            if not os.path.exists(filename):
                with open(filename, 'wb') as f:
                    img = requests.get(item).content
                    f.write(img)
            j += 1

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

    def run(self):
        if not os.path.exists(self.dir_name):
            os.mkdir(self.dir_name)

        self.get_picture_detail_list()

        threads = []
        for info in self.picture_detail_url:
            # 实例化对象，target=目标函数名，args=目标函数参数(元组格式)
            t = threading.Thread(target=self.download, args=(info,))
            threads.append(t)
            t.start()

        # 等待所有子线程结束再运行主线程
        [thread.join() for thread in threads]

if __name__ == '__main__':
    ku().hello().run()