#!/usr/bin/env python
# encoding: utf-8
'''
#-------------------------------------------------------------------
#                   CONFIDENTIAL --- CUSTOM STUDIOS
#-------------------------------------------------------------------
#
#                   @Project Name : 博客之星点赞
#
#                   @File Name    : main.py
#
#                   @Programmer   : autofelix
#
#                   @Start Date   : 2021/12/30 14:42
#
#                   @Last Update  : 2021/12/30 14:42
#
#-------------------------------------------------------------------
'''
import time,random
from selenium import webdriver
from selenium.webdriver import ActionChains

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
        print(' ' * 15 + 'csdn博客之星点赞脚本')
        print(' ' * 5 + 'Author: autofelix  Date: 2021-12-30 14:42')
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
        driver = self.init_driver()
        print('-----请先手动登录-----')
        driver.get('https://passport.csdn.net/newlogin')
        time.sleep(10)
        driver.get('https://bbs.csdn.net/topics/603961577')
        self.start(driver)

    def start(self, driver):
        time.sleep(3)
        ActionChains(driver).move_to_element(driver.find_element_by_xpath('//*[@id="floor-user-content_562"]/div/div[3]/div[1]/div[1]/div/div[2]/div[2]')).perform()
        driver.find_element_by_xpath('//*[@id="floor-user-content_562"]/div/div[3]/div[1]/div[1]/div/div[1]/div[2]/div[3]/div[2]/span[1]/i').click()
        driver.find_element_by_xpath('//*[@id="floor-user-content_562"]/div/div[3]/div[1]/div[1]/div/div[2]/div[1]/div[2]/a').click()
        print('访问结束：' + driver.current_url)
        self.start(driver)

if __name__ == "__main__":
    csdn().hello().run()
