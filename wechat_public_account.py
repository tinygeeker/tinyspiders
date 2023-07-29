#!/usr/bin/env python
# encoding: utf-8
'''
#-------------------------------------------------------------------
#                   CONFIDENTIAL --- CUSTOM STUDIOS
#-------------------------------------------------------------------
#
#                   @Project Name : 获取微信公众平台原创文章
#
#                   @File Name    : wechat_public_account.py
#
#                   @Programmer   : tinygeeker
#
#                   @Start Date   : 2022/01/11 13:14
#
#                   @Last Update  : 2022/01/11 13:14
#
#-------------------------------------------------------------------
'''
import json, time, pdfkit, requests

class wechatPublic:
    '''
     This is a main Class, the file contains all documents.
     One document contains paragraphs that have several sentences
     It loads the original file and converts the original file to new content
     Then the new content will be saved by this class
    '''
    def __init__(self):
        self.url = 'https://mp.weixin.qq.com/mp/profile_ext'
        # 这些信息不能抄我的，要用你自己的才有效
        self.headers = {
            'Connection': 'keep - alive',
            'Accept': '* / *',
            'User-Agent': '写你自己的',
            'Referer': '写你自己的',
            'Accept-Encoding': 'br, gzip, deflate'
        }
        self.cookies = {
            'devicetype': 'iOS12.2',
            'lang': 'zh_CN',
            'pass_ticket': '写你自己的',
            'version': '1700042b',
            'wap_sid2': '写你自己的',
            'wxuin': '3340537333'
        }

    def hello(self):
        '''
        This is a welcome speech
        :return: self
        '''
        print('*' * 50)
        print(' ' * 10 + '获取微信公众平台原创文章')
        print(' ' * 5 + '作者: tinygeeker  Date: 2022-01-11 13:14')
        print(' ' * 5 + '主页: https://tinygeeker.blog.csdn.net')
        print('*' * 50)
        return self

    def run(self):
        '''
        program entry
        '''
        self.get_list_data(0)

    def get_params(self, offset):
        '''
        Get params
        '''
        params = {
            'action': 'getmsg',
            '__biz': '写你自己的',
            'offset': '{}'.format(offset),
            'count': '10',
            'is_ok': '1',
            'scene': '126',
            'uin': '777',
            'key': '777',
            'pass_ticket': '写你自己的',
            'appmsg_token': '写你自己的',
            'x5': '0',
            'f': 'json',
        }

        return params


    def get_list_data(self, offset):
        '''
        Get list data
        '''
        response = requests.get(self.url, headers=self.headers, params=self.get_params(offset), cookies=self.cookies)
        data = json.loads(response.text)
        can_msg_continue = data['can_msg_continue']
        next_offset = data['next_offset']

        general_msg_list = data['general_msg_list']
        list_data = json.loads(general_msg_list)['list']

        for data in list_data:
            try:
                if data['app_msg_ext_info']['copyright_stat'] == 11:
                    msg_info = data['app_msg_ext_info']
                    title = msg_info['title']
                    content_url = msg_info['content_url']
                    # 自己定义存储路径
                    pdfkit.from_url(content_url, '/home/wistbean/wechat_article/'+title+'.pdf')
                    print('获取到原创文章：%s ： %s' % (title, content_url))
            except:
                print('不是图文')

        if can_msg_continue == 1:
            time.sleep(1)
            self.get_list_data(next_offset)


if __name__ == '__main__':
    wechatPublic().hello().run()