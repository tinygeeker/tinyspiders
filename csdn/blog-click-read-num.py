#!/usr/bin/env python
# encoding: utf-8
'''
#-------------------------------------------------------------------
#                   CONFIDENTIAL --- CUSTOM STUDIOS                      
#-------------------------------------------------------------------
#                                                                   
#                   @Project Name : 线程增加阅读量点击量
#                                                                   
#                   @File Name    : blog-click-read-num.py
#                                                                   
#                   @Programmer   : tinygeeker                           
#                                                                     
#                   @Start Date   : 2022/01/05 13:14
#                                                                   
#                   @Last Update  : 2022/01/05 13:14
#                                                                   
#-------------------------------------------------------------------
'''
import time, random, threading
from selenium import webdriver


class csdn:
    '''
     This is a main Class, the file contains all documents.
     One document contains paragraphs that have several sentences
     It loads the original file and converts the original file to new content
     Then the new content will be saved by this class
    '''
    def __init__(self):
        self.userAgent = [
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            # 谷歌
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',  # 火狐
            'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',  # IE
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
            # 360
        ]

    def hello(self):
        '''
        This is a welcome speech
        :return: self
        '''
        print('*' * 50)
        print(' ' * 15 + 'csdn线程阅读量点击量阅读量')
        print(' ' * 5 + '作者: tinygeeker  Date: 2022-01-05 13:14')
        print(' ' * 5 + '主页: https://tinygeeker.blog.csdn.net')
        print('*' * 50)
        return self

    def init_driver(self):
        '''
        The browser setting
        '''
        chrome_options = webdriver.ChromeOptions()

        # 关掉浏览器左上角的通知提示，如上图
        chrome_options.add_experimental_option('prefs', {
            'profile.default_content_setting_values': {'notifications': 2}
        })

        # 关闭'chrome正受到自动测试软件的控制'提示
        chrome_options.add_argument('disable-infobars')

        # 设置浏览器请求头
        chrome_options.add_argument("user-agent={}".format(random.choices(self.userAgent)))

        # 后台运行
        # chrome_options.add_argument('headless')

        return webdriver.Chrome(options=chrome_options)

    def run(self):
        '''
        The program entry
        '''
        blogerUrl = input('请输入博主主页地址：') or 'https://tinygeeker.blog.csdn.net'
        while True:
            t1 = threading.Thread(target=self.start, args=(self.init_driver(), blogerUrl,))
            t2 = threading.Thread(target=self.start, args=(self.init_driver(), blogerUrl,))
            t3 = threading.Thread(target=self.start, args=(self.init_driver(), blogerUrl,))
            t1.start()
            t2.start()
            t3.start()
            t1.join()
            t2.join()
            t3.join()

    def start(self, driver, url):
        '''
        The program run
        '''
        driver.get(url)
        time.sleep(3)
        # 适用于csdn新版主页
        articles = driver.find_elements_by_class_name('blog-list-box')[0:3]
        try:
            for article in articles:
                article.find_element_by_tag_name('h4').click()
                time.sleep(5)
        except Exception as e:
            print(e)
        finally:
            driver.quit()

if __name__ == "__main__":
    csdn().hello().run()
