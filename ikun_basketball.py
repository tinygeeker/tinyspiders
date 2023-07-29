#!/usr/bin/env python
# encoding: utf-8
'''
#-------------------------------------------------------------------
#                   CONFIDENTIAL --- CUSTOM STUDIOS
#-------------------------------------------------------------------
#
#                   @Project Name : 爬取蔡徐坤打篮球相关视频
#
#                   @File Name    : ikun_basketball.py
#
#                   @Programmer   : autofelix
#
#                   @Start Date   : 2022/01/10 13:14
#
#                   @Last Update  : 2022/01/10 13:14
#
#-------------------------------------------------------------------
'''
import xlwt
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

book = xlwt.Workbook(encoding='utf-8', style_compression=0)

sheet = book.add_sheet('蔡徐坤篮球', cell_overwrite_ok=True)
sheet.write(0, 0, '名称')
sheet.write(0, 1, '地址')
sheet.write(0, 2, '描述')
sheet.write(0, 3, '观看次数')
sheet.write(0, 4, '弹幕数')
sheet.write(0, 5, '发布时间')

n = 1

class basketball:
    '''
     This is a main Class, the file contains all documents.
     One document contains paragraphs that have several sentences
     It loads the original file and converts the original file to new content
     Then the new content will be saved by this class
    '''
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.WAIT = WebDriverWait(self.browser, 10)

    def hello(self):
        '''
        This is a welcome speech
        :return: self
        '''
        print('*' * 50)
        print(' ' * 10 + '爬取蔡徐坤打篮球相关视频')
        print(' ' * 5 + '作者: tinygeeker  Date: 2022-01-10 13:14')
        print(' ' * 5 + '主页: https://tinygeeker.blog.csdn.net')
        print('*' * 50)
        return self

    def run(self):
        '''
        program entry
        '''
        self.browser.set_window_size(1400, 900)
        try:
            total = self.search()
            for i in range(2, int(total + 1)):
                self.next_page(i)
        finally:
            self.browser.close()
        book.save('蔡徐坤篮球.xlsx')

    def search(self):
        '''
        Search the keywords
        '''
        try:
            print('开始访问b站....')
            self.browser.get("https://www.bilibili.com/")

            input = self.WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#nav_searchform > input")))
            submit = self.WAIT.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/div/div[1]/div[1]/div/div[2]/div/form/div/button')))

            input.send_keys('蔡徐坤 篮球')
            submit.click()

            # 跳转到新的窗口
            print('跳转到新窗口')
            all_h = self.browser.window_handles
            self.browser.switch_to.window(all_h[1])
            self.get_source()

            total = self.WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                               "#all-list > div.flow-loader > div.page-wrap > div > ul > li.page-item.last > button")))
            return int(total.text)
        except TimeoutException:
            return self.search()


    def next_page(self, page_num):
        '''
        Jump to next page
        '''
        try:
            print('获取下一页数据')
            next_btn = self.WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                              '#all-list > div.flow-loader > div.page-wrap > div > ul > li.page-item.next > button')))
            next_btn.click()
            self.WAIT.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,
                                                         '#all-list > div.flow-loader > div.page-wrap > div > ul > li.page-item.active > button'),
                                                        str(page_num)))
            self.get_source()
        except TimeoutException:
            self.browser.refresh()
            return self.next_page(page_num)


    def save_to_excel(self, soup):
        '''
        Save the info to excel
        '''
        list = soup.find(class_='video-list clearfix').find_all(class_='video-item matrix')

        for item in list:
            item_title = item.find('a').get('title')
            item_link = item.find('a').get('href')
            item_dec = item.find(class_='des hide').text
            item_view = item.find(class_='so-icon watch-num').text
            item_biubiu = item.find(class_='so-icon hide').text
            item_date = item.find(class_='so-icon time').text

            print('爬取：' + item_title)

            global n

            sheet.write(n, 0, item_title)
            sheet.write(n, 1, item_link)
            sheet.write(n, 2, item_dec)
            sheet.write(n, 3, item_view)
            sheet.write(n, 4, item_biubiu)
            sheet.write(n, 5, item_date)

            n = n + 1

    def get_source(self):
        '''
        Get the source
        '''
        self.WAIT.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#all-list > div.flow-loader > div.filter-wrap')))

        html = self.browser.page_source
        soup = BeautifulSoup(html, 'lxml')
        self.save_to_excel(soup)

if __name__ == '__main__':
    basketball().hello().run()
