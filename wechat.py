#!/usr/bin/env python
# encoding: utf-8
'''
#-------------------------------------------------------------------
#                   CONFIDENTIAL --- CUSTOM STUDIOS
#-------------------------------------------------------------------
#
#                   @Project Name : 获取指定用户的微信数据
#
#                   @File Name    : wechat_moment.py
#
#                   @Programmer   : autofelix
#
#                   @Start Date   : 2022/01/10 13:14
#
#                   @Last Update  : 2022/01/10 13:14
#
#-------------------------------------------------------------------
'''
import time
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class wechat():
    '''
     This is a main Class, the file contains all documents.
     One document contains paragraphs that have several sentences
     It loads the original file and converts the original file to new content
     Then the new content will be saved by this class
    '''
    def __init__(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '5.1'
        desired_caps['deviceName'] = '88CKBM622PAM'
        desired_caps['appPackage'] = 'com.tencent.mm'
        desired_caps['appActivity'] = '.ui.LauncherUI'

        # 定义在朋友圈的时候滑动位置
        self.start_x = 300
        self.start_y = 800
        self.end_x = 300
        self.end_y = 300

        # 启动微信
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        # 设置等待
        self.wait = WebDriverWait(self.driver, 300)

    def hello(self):
        '''
        This is a welcome speech
        :return: self
        '''
        print('*' * 50)
        print(' ' * 10 + '获取指定用户的微信数据')
        print(' ' * 5 + '作者: autofelix  Date: 2022-01-10 13:14')
        print(' ' * 5 + '主页: https://autofelix.blog.csdn.net')
        print('*' * 50)
        return self

    def login(self, uname, pwd):
        '''
        Login wechat
        '''
        # 获取到登录按钮后点击
        print('开始登录...')
        login_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/e4g")))
        login_btn.click()
        # 获取使用微信号登录按钮
        change_login_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/cou")))
        change_login_btn.click()
        # 获取输入账号元素并输入
        account = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@resource-id="com.tencent.mm:id/cos"]/android.widget.EditText')))
        account.send_keys(uname)
        # 获取密码元素并输入
        password = self.wait.until(EC.presence_of_element_located((By.XPATH,  '//*[@resource-id="com.tencent.mm:id/cot"]/android.widget.EditText')))
        password.send_keys(pwd)
        # 登录
        login = self.wait.until(EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/cov")))
        login.click()
        # 点击去掉通讯录提示框
        no_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/az9")))
        no_btn.click()
        print('登录成功...')

    def search(self, keywords):
        '''
        Enter the club of keywords
        '''
        # 获取到搜索按钮后点击
        search_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/iq")))
        # 等搜索建立索引再点击
        time.sleep(10)
        search_btn.click()
        # 获取搜索框并输入
        print('正在搜索...')
        search_input = self.wait.until(EC.presence_of_element_located((By.ID, "com.tencent.mm:id/kh")))
        search_input.send_keys(keywords)
        # 点击头像进入
        key_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/py")))
        key_btn.click()
        # 点击右上角...进入
        menu_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/jy")))
        menu_btn.click()
        # 再点击头像
        icon_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/e0c")))
        icon_btn.click()
        # 点击朋友圈
        moment_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/d86")))
        moment_btn.click()
        print('进入朋友圈...')

    def get_data(self):
        '''
        Get the data of club
        '''
        while True:
            # 获取 ListView
            items = self.wait.until(EC.presence_of_all_elements_located((By.ID, 'com.tencent.mm:id/eew')))
            # 滑动
            self.driver.swipe(self.start_x, self.start_y, self.end_x, self.end_y, 2000)
            #遍历获取每个List数据
            for item in items:
                moment_text = item.find_element_by_id('com.tencent.mm:id/kt').text
                day_text = item.find_element_by_id('com.tencent.mm:id/eke').text
                month_text = item.find_element_by_id('com.tencent.mm:id/ekf').text
                print('抓取到其朋友圈数据： %s' % moment_text)
                print('抓取到其发布时间： %s月%s' % (month_text, day_text))

if __name__ == '__main__':
    wx = wechat().hello()
    uname = input('请输入登录账号：')
    pwd = input('请输入登录密码：')
    wx.login(uname, pwd)
    keywords = input('请输入搜索关键字：')
    wx.search(keywords)
    wx.get_data()











