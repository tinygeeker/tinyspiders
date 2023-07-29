#!/usr/bin/env python
# encoding: utf-8
'''
#-------------------------------------------------------------------
#                   CONFIDENTIAL --- CUSTOM STUDIOS                      
#-------------------------------------------------------------------
#                                                                   
#                   @Project Name : 线程增加博客阅读量
#                                                                   
#                   @File Name    : add_blog_read_num.py
#                                                                   
#                   @Programmer   : tinygeeker                           
#                                                                     
#                   @Start Date   : 2023/07/29 13:14
#                                                                   
#                   @Last Update  : 2022/07/29 13:14
#                                                                   
#-------------------------------------------------------------------
'''
import time, random, requests
from retrying import retry
from fake_useragent import UserAgent

class AddBlogReadNum:
    '''
     This is a main Class, the file contains all documents.
     One document contains paragraphs that have several sentences
     It loads the original file and converts the original file to new content
     Then the new content will be saved by this class
    '''
    def __init__(self):
        pass

    def hello(self):
        '''
        This is a welcome speech
        :return: self
        '''
        print('*' * 50)
        print(' ' * 15 + 'csdn线程阅读量点击量阅读量')
        print(' ' * 5 + '作者: tinygeeker  Date: 2023/07/29 13:14')
        print(' ' * 5 + '主页: https://tinygeeker.blog.csdn.net')
        print('*' * 50)
        return self

    def run(self):
        '''
        The program entry
        '''
        url = input('请输入想增加阅读量的文章地址链接：') or 'https://tinygeeker.blog.csdn.net/article/details/131053143'

        while True:
            self.request(url)
            time.sleep(10)


    @retry(stop_max_attempt_number=3)
    def request(self, url):
        '''
        Send a request
        :param url: the url of request
        :return: the text of request
        '''
        try:
            headers = {
                'User-Agent': UserAgent().random
            }
            response = requests.get(url, timeout=10, headers=headers)
            assert response.status_code == 200
            response.encoding = 'gbk'
            return response.text
        except:
            pass



if __name__ == "__main__":
    AddBlogReadNum().hello().run()
