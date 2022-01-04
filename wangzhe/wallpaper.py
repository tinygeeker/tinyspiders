#!/usr/bin/env python
# encoding: utf-8
'''
#-------------------------------------------------------------------
#                   CONFIDENTIAL --- CUSTOM STUDIOS
#-------------------------------------------------------------------
#
#                   @Project Name : 王者荣耀壁纸下载
#
#                   @File Name    : wallpaper.py
#
#                   @Programmer   : autofelix
#
#                   @Start Date   : 2021-01-04 13:14
#
#                   @Last Update  : 2021-01-04 13:14
#
#-------------------------------------------------------------------
'''
import os, time, requests, json, re
from retrying import retry
from urllib import parse

class HonorOfKings:
    '''
     This is a main Class, the file contains all documents.
     One document contains paragraphs that have several sentences
     It loads the original file and converts the original file to new content
     Then the new content will be saved by this class
    '''
    def __init__(self, save_path='./heros'):
        self.save_path = save_path
        self.time = str(time.time()).split('.')
        self.url = 'https://apps.game.qq.com/cgi-bin/ams/module/ishow/V1.0/query/workList_inc.cgi?activityId=2735&sVerifyCode=ABCD&sDataType=JSON&iListNum=20&totalpage=0&page={}&iOrder=0&iSortNumClose=1&iAMSActivityId=51991&_everyRead=true&iTypeId=2&iFlowId=267733&iActId=2735&iModuleId=2735&_=%s' % self.time[0]

    def hello(self):
        '''
        This is a welcome speech
        :return: self
        '''
        print('\033[1;30;46m')
        print("*" * 50)
        print(' ' * 18 + '王者荣耀壁纸下载')
        print(' ' * 5 + '作者: autofelix  Date: 2021-01-04 13:14')
        print("*" * 50)
        print('\033[0m')
        return self

    def run(self):
        '''
        The program entry
        '''
        print('↓' * 20 + ' 格式选择: ' + '↓' * 20)
        print('1.缩略图 2.1024x768 3.1280x720 4.1280x1024 5.1440x900 6.1920x1080 7.1920x1200 8.1920x1440')
        size = input('请输入您想下载的格式序号，默认6：')
        size = size if size and int(size) in [1,2,3,4,5,6,7,8] else 6

        print('---下载开始...')
        page = 0
        offset = 0
        main_response = self.request(self.url.format(page)).text
        main_detail = json.loads(main_response)
        total_page = --int(main_detail['iTotalPages'])
        print('---总共 {} 页...' . format(total_page))
        while True:
            if offset > total_page:
                break
            url = self.url.format(offset)
            response = self.request(url).text
            result = json.loads(response)
            now = 0
            for item in result["List"]:
                now += 1
                hero_name = parse.unquote(item['sProdName']).split('-')[0]
                hero_name = re.sub(r'[【】:.<>|·@#$%^&() ]', '', hero_name)
                print('---正在下载第 {} 页 {} 英雄 进度{}/{}...' . format(offset + 1, hero_name, now, len(result["List"])))
                hero_url = parse.unquote(item['sProdImgNo_{}'.format(str(size))])
                save_path = self.save_path + '/' + hero_name
                save_name = save_path + '/' + hero_url.split('/')[-2]
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
                if not os.path.exists(save_name):
                    with open(save_name, 'wb') as f:
                        response_content = self.request(hero_url.replace("/200", "/0")).content
                        f.write(response_content)
            offset += 1
        print('---下载完成...')

    @retry(stop_max_attempt_number=3)
    def request(self, url):
        '''
        Send a request
        :param url: the url of request
        :param timeout: the time of request
        :return: the result of request
        '''
        response = requests.get(url, timeout=10)
        assert response.status_code == 200
        return response

if __name__ == "__main__":
    HonorOfKings().hello().run()
