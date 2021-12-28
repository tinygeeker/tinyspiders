#!/usr/bin/env python
# encoding: utf-8
'''
#-------------------------------------------------------------------
#                   CONFIDENTIAL --- CUSTOM STUDIOS                      
#-------------------------------------------------------------------
#                                                                   
#                   @Project Name : 抖音下载小助手
#                                                                   
#                   @File Name    : main.py                      
#                                                                   
#                   @Programmer   : autofelix
#                                                                     
#                   @Start Date   : 2020/7/30 14:42                 
#                                                                   
#                   @Last Update  : 2020/7/30 14:42                 
#                                                                   
#-------------------------------------------------------------------
'''
import os, sys, requests
import json, re, time
from retrying import retry
from contextlib import closing

class DouYin:
    '''
     This is a main Class, the file contains all documents.
     One document contains paragraphs that have several sentences
     It loads the original file and converts the original file to new content
     Then the new content will be saved by this class
    '''
    def __init__(self):
        '''
        Initial the custom file by some url
        '''
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        }

    def hello(self):
        '''
        This is welcome speech
        :return: self
        '''
        print("*" * 50)
        print(' ' * 15 + '抖音下载小助手')
        print(' ' * 5 + '作者: autofelix  Date: 2020-05-20 13:14')
        print(' ' * 15 + '无水印 | 有水印')
        print(' ' * 12 + '输入用户的sec_uid即可')
        print(' ' * 2 + '用浏览器打开用户分享链接，复制参数中sec_uid')
        print("*" * 50)
        return self

    def get_video_urls(self, sec_uid, type_flag='p'):
        '''
        Get the video link of user
        :param type_flag: the type of video
        :return: nickname, video_list
        '''
        user_url_prefix = 'https://www.iesdouyin.com/web/api/v2/aweme/post' if type_flag == 'p' else 'https://www.iesdouyin.com/web/api/v2/aweme/like'
        print('---解析视频链接中...\r')

        i = 0
        result = []
        while result == []:
            i = i + 1
            print('---正在第 {} 次尝试...\r'.format(str(i)))
            user_url = user_url_prefix + '/?sec_uid=%s&count=2000' % (sec_uid)
            response = self.get_request(user_url)
            html = json.loads(response.content.decode())
            if html['aweme_list'] != []:
                result = html['aweme_list']

        nickname = None
        video_list = []
        for item in result:
            if nickname is None:
                nickname = item['author']['nickname'] if re.sub(r'[\/:*?"<>|]', '', item['author']['nickname']) else None

            video_list.append({
                'desc': re.sub(r'[\/:*?"<>|]', '', item['desc']) if item['desc'] else '无标题' + str(int(time.time())),
                'url': item['video']['play_addr']['url_list'][0]
            })
        return nickname, video_list

    def get_download_url(self, video_url, watermark_flag):
        '''
        Whether to download watermarked videos
        :param video_url: the url of video
        :param watermark_flag: the type of video
        :return: the url of o
        '''
        if watermark_flag == True:
            download_url = video_url.replace('api.amemv.com', 'aweme.snssdk.com')
        else:
            download_url = video_url.replace('aweme.snssdk.com', 'api.amemv.com')

        return download_url

    def video_downloader(self, video_url, video_name, watermark_flag=False):
        '''
        Download the video
        :param video_url: the url of video
        :param video_name: the name of video
        :param watermark_flag: the flag of video
        :return: None
        '''
        size = 0
        video_url = self.get_download_url(video_url, watermark_flag=watermark_flag)
        with closing(requests.get(video_url, headers=self.headers, stream=True)) as response:
            chunk_size = 1024
            content_size = int(response.headers['content-length'])
            if response.status_code == 200:
                sys.stdout.write('----[文件大小]:%0.2f MB\n' % (content_size / chunk_size / 1024))

                with open(video_name + '.mp4', 'wb') as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        size += len(data)
                        file.flush()

                        sys.stdout.write('----[下载进度]:%.2f%%' % float(size / content_size * 100) + '\r')
                        sys.stdout.flush()

    @retry(stop_max_attempt_number=3)
    def get_request(self, url, params=None):
        '''
        Send a get request
        :param url: the url of request
        :param params: the params of request
        :return: the result of request
        '''
        if params is None:
            params = {}
        response = requests.get(url, params=params, headers=self.headers, timeout=10)
        assert response.status_code == 200
        return response

    @retry(stop_max_attempt_number=3)
    def post_request(self, url, data=None):
        '''
        Send a post request
        :param url: the url of request
        :param data: the params of request
        :return: the result of request
        '''
        if data is None:
            data = {}
        response = requests.post(url, data=data, headers=self.headers, timeout=10)
        assert response.status_code == 200
        return response

    def run(self):
        '''
        Program entry
        '''
        sec_uid = input('请输入用户sec_uid:')
        sec_uid = sec_uid if sec_uid else 'MS4wLjABAAAAle_oORaZCgYlB84cLTKSqRFvDgGmgrJsS6n3TfwxonM'

        watermark_flag = input('是否下载带水印的视频 (0-否(默认), 1-是):')
        watermark_flag = bool(int(watermark_flag)) if watermark_flag else 0

        type_flag = input('p-上传的(默认), l-收藏的:')
        type_flag = type_flag if type_flag else 'p'

        save_dir = input('保存路径 (默认"./Download/"):')
        save_dir = save_dir if save_dir else "./Download/"

        nickname, video_list = self.get_video_urls(sec_uid, type_flag)
        nickname_dir = os.path.join(save_dir, nickname)

        if not os.path.exists(nickname_dir):
            os.makedirs(nickname_dir)

        if type_flag == 'f':
            if 'favorite' not in os.listdir(nickname_dir):
                os.mkdir(os.path.join(nickname_dir, 'favorite'))

        print('---视频下载中: 共有%d个作品...\r' % len(video_list))

        for num in range(len(video_list)):
            print('---正在解析第%d个视频链接 [%s] 中，请稍后...\n' % (num + 1, video_list[num]['desc']))

            video_path = os.path.join(nickname_dir, video_list[num]['desc']) if type_flag != 'f' else os.path.join(nickname_dir, 'favorite', video_list[num]['desc'])
            if os.path.isfile(video_path):
                print('---视频已存在...\r')
            else:
                self.video_downloader(video_list[num]['url'], video_path, watermark_flag)
            print('\n')
        print('---下载完成...\r')

if __name__ == "__main__":
    DouYin().hello().run()