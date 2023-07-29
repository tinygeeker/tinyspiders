#!/usr/bin/env python
# encoding: utf-8
'''
#-------------------------------------------------------------------
#                   CONFIDENTIAL --- CUSTOM STUDIOS
#-------------------------------------------------------------------
#
#                   @Project Name : 破解哔哩哔哩登录滑动验证码
#
#                   @File Name    : bilibili_captcha_crack.py
#
#                   @Programmer   : tinygeeker
#
#                   @Start Date   : 2022/01/11 13:14
#
#                   @Last Update  : 2022/01/11 13:14
#
#-------------------------------------------------------------------
'''
import time, requests, re
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from io import BytesIO

class bilibili:
    def __init__(self):
        '''
         This is a main Class, the file contains all documents.
         One document contains paragraphs that have several sentences
         It loads the original file and converts the original file to new content
         Then the new content will be saved by this class
        '''
        self.driver = webdriver.Chrome()
        self.WAIT = WebDriverWait(self.driver, 10)
        self.url = 'https://passport.bilibili.com/login'

    def hello(self):
        '''
        This is a welcome speech
        :return: self
        '''
        print('*' * 50)
        print(' ' * 20 + '破解哔哩哔哩登录滑动验证码')
        print(' ' * 5 + '作者: tinygeeker  Date: 2022-01-09 13:14')
        print(' ' * 5 + '主页: https://tinygeeker.blog.csdn.net')
        print('*' * 50)
        return self

    def run(self):
        '''
        program entry
        '''
        self.driver.get(self.url)
        slider = self.WAIT.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#gc-box > div > div.gt_slider > div.gt_slider_knob.gt_show")))
        self.recognize_code(self.driver)


    def mergy_Image(self, image_file, location_list):
        """
        将原始图片进行合成
        :param image_file: 图片文件
        :param location_list: 图片位置
        :return: 合成新的图片
        """
        # 存放上下部分的各个小块
        upper_half_list = []
        down_half_list = []

        image = Image.open(image_file)

        # 通过 y 的位置来判断是上半部分还是下半部分,然后切割
        for location in location_list:
            if location['y'] == -58:
                # 间距为10，y：58-116
                im = image.crop((abs(location['x']), 58, abs(location['x'])+10, 116))
                upper_half_list.append(im)
            if location['y'] == 0:
                # 间距为10，y：0-58
                im = image.crop((abs(location['x']), 0, abs(location['x']) + 10, 58))
                down_half_list.append(im)

        # 创建一张大小一样的图片
        new_image = Image.new('RGB', (260, 116))

        # 粘贴好上半部分 y坐标是从上到下（0-116）
        offset = 0
        for im in upper_half_list:
            new_image.paste(im, (offset, 0))
            offset += 10

        # 粘贴好下半部分
        offset = 0
        for im in down_half_list:
            new_image.paste(im, (offset, 58))
            offset += 10

        return new_image

    def get_distance(self, bg_Image, fullbg_Image):
        '''
        Get distance
        '''
        threshold = 200

        print(bg_Image.size[0])
        print(bg_Image.size[1])


        for i in range(60, bg_Image.size[0]):
            for j in range(bg_Image.size[1]):
                bg_pix = bg_Image.getpixel((i, j))
                fullbg_pix = fullbg_Image.getpixel((i, j))
                r = abs(bg_pix[0] - fullbg_pix[0])
                g = abs(bg_pix[1] - fullbg_pix[1])
                b = abs(bg_pix[2] - fullbg_pix[2])

                if r + g + b > threshold:
                   return i

    def get_path(self, distance):
        '''
        Get path
        '''
        result = []
        current = 0
        mid = distance * 4 / 5
        t = 0.2
        v = 0
        while current < (distance - 10):
            if current < mid:
                a = 2
            else:
                a = -3
            v0 = v
            v = v0 + a * t
            s = v0 * t + 0.5 * a * t * t
            current += s
            result.append(round(s))
        return result

    def start_drag(self, driver, distance):
        '''
        Start drag
        '''
        knob = self.WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#gc-box > div > div.gt_slider > div.gt_slider_knob.gt_show")))
        result = self.get_path(distance)
        ActionChains(driver).click_and_hold(knob).perform()

        for x in result:
            ActionChains(driver).move_by_offset(xoffset=x, yoffset=0).perform()

        time.sleep(0.5)
        ActionChains(driver).release(knob).perform()

    def recognize_code(self, driver):
        '''
        Recognize code
        '''
        bs = BeautifulSoup(driver.page_source,'lxml')
        # 找到背景图片和缺口图片的div
        bg_div = bs.find_all(class_='gt_cut_bg_slice')
        fullbg_div = bs.find_all(class_='gt_cut_fullbg_slice')

        # 获取缺口背景图片url
        bg_url = re.findall('background-image:\surl\("(.*?)"\)',bg_div[0].get('style'))
        # 获取背景图片url
        fullbg_url = re.findall('background-image:\surl\("(.*?)"\)',fullbg_div[0].get('style'))

        # 存放每个合成缺口背景图片的位置
        bg_location_list = []
        # 存放每个合成背景图片的位置
        fullbg_location_list = []

        for bg in bg_div:
            location = {}
            location['x'] = int(re.findall('background-position:\s(.*?)px\s(.*?)px;', bg.get('style'))[0][0])
            location['y'] = int(re.findall('background-position:\s(.*?)px\s(.*?)px;', bg.get('style'))[0][1])
            bg_location_list.append(location)

        for fullbg in fullbg_div:
            location = {}
            location['x'] = int(re.findall('background-position:\s(.*?)px\s(.*?)px;', fullbg.get('style'))[0][0])
            location['y'] = int(re.findall('background-position:\s(.*?)px\s(.*?)px;', fullbg.get('style'))[0][1])
            fullbg_location_list.append(location)

        print(bg_location_list)
        print(fullbg_location_list)

        # 将图片格式存为 jpg 格式
        bg_url = bg_url[0].replace('webp', 'jpg')
        fullbg_url = fullbg_url[0].replace('webp', 'jpg')
        # print(bg_url)
        # print(fullbg_url)

        # 下载图片
        bg_image = requests.get(bg_url).content
        fullbg_image = requests.get(fullbg_url).content
        print('完成图片下载')

        # 写入图片
        bg_image_file = BytesIO(bg_image)
        fullbg_image_file = BytesIO(fullbg_image)

        # 合成图片
        bg_Image = self.mergy_Image(bg_image_file, bg_location_list)
        fullbg_Image = self.mergy_Image(fullbg_image_file, fullbg_location_list)

        # 计算缺口偏移距离
        distance = self.get_distance(bg_Image, fullbg_Image)
        print('得到距离：%s' % str(distance))
        self.start_drag(driver, distance)

if __name__ == '__main__':
    bilibili().hello().run()