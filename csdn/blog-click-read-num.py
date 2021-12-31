#!/usr/bin/env python
# encoding: utf-8
'''
#-------------------------------------------------------------------
#                   CONFIDENTIAL --- CUSTOM STUDIOS                      
#-------------------------------------------------------------------
#                                                                   
#                   @Project Name : 线程阅读量点击量
#                                                                   
#                   @File Name    : csdn.py                      
#                                                                   
#                   @Programmer   : autofelix                           
#                                                                     
#                   @Start Date   : 2021/4/30 11:05                 
#                                                                   
#                   @Last Update  : 2021/4/30 11:05                 
#                                                                   
#-------------------------------------------------------------------
'''
import time,random,threading
from selenium import webdriver

class csdn:
    def __init__(self):
        self.userAgent = [
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36', #谷歌
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0', #火狐
            'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko', #IE
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36' #360
        ]

    def hello(self):
        print("*" * 50)
        print(' ' * 15 + 'csdn线程阅读量点击量阅读量')
        print(' ' * 5 + 'Author: autofelix  Date: 2020-05-20 13:14')
        print("*" * 50)
        return self

    def init_driver(self):
        chrome_options = webdriver.ChromeOptions()

        # 关掉浏览器左上角的通知提示，如上图
        chrome_options.add_experimental_option('prefs', {'profile.default_content_setting_values': {'notifications': 2}})

        # 关闭'chrome正受到自动测试软件的控制'提示
        chrome_options.add_argument('disable-infobars')

        # 设置浏览器请求头
        chrome_options.add_argument("user-agent={}".format(random.choices(self.userAgent)))

        # 后台运行
        # chrome_options.add_argument('headless')

        return webdriver.Chrome(options=chrome_options)

    def run(self):
        while True:
            t1 = threading.Thread(target=self.start, args=(self.init_driver(),))
            t2 = threading.Thread(target=self.start, args=(self.init_driver(),))
            # t3 = threading.Thread(target=self.start, args=(self.init_driver(),))
            t1.start()
            t2.start()
            # t3.start()
            t1.join()
            t2.join()
            # t3.join()

    def start(self, driver):
        driver.get('https://autofelix.blog.csdn.net')
        time.sleep(3)
        # driver.find_element_by_class_name('csdn-redpack-close').click()

        # main_window = driver.current_window_handle

        articles = driver.find_elements_by_class_name('csdn-tracking-statistics')[19:23]
        try:
            for article in articles:
                # 点击量
                article.find_element_by_tag_name('h4').click()
                # driver.s witch_to.window(driver.window_handles[-1])

                time.sleep(5)
                # driver.close()
                # driver.switch_to.window(main_window)

        except Exception as e:
            print(e)
        finally:
            driver.quit()

if __name__ == "__main__":
    csdn().hello().run()
