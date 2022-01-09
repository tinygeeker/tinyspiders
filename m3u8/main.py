#!/usr/bin/env python
# encoding: utf-8
'''
#-------------------------------------------------------------------
#                   CONFIDENTIAL --- CUSTOM STUDIOS
#-------------------------------------------------------------------
#
#                   @Project Name : 多进程M3U8视频下载助手
#
#                   @File Name    : main.py
#
#                   @Programmer   : autofelix
#
#                   @Start Date   : 2022/01/05 13:14
#
#                   @Last Update  : 2022/01/05 13:14
#
#-------------------------------------------------------------------
'''
import os, platform
import time, requests
import multiprocessing
from retrying import retry
from Crypto.Cipher import AES

class M3u8:
    '''
     This is a main Class, the file contains all documents.
     One document contains paragraphs that have several sentences
     It loads the original file and converts the original file to new content
     Then the new content will be saved by this class
    '''
    def __init__(self):
        '''
        Initial the custom file by self
        '''
        self.encrypt = False
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0"
        }

    def hello(self):
        '''
        This is a welcome speech
        :return: self
        '''
        print('*' * 50)
        print(' ' * 15 + 'm3u8链接下载小助手')
        print(' ' * 5 + '作者: autofelix  Date: 2022-01-05 13:14')
        print(' ' * 5 + '主页: https://autofelix.blog.csdn.net')
        print(' ' * 12 + '适用于非加密 | 加密链接')
        print('*' * 50)
        return self

    def checkUrl(self, url):
        '''
        Determine if it is a available link of m3u8
        :return: bool
        '''
        if '.m3u8' not in url:
            return False
        elif not url.startswith('http'):
            return False
        else:
            return True

    def parse(self, url):
        '''
        Analyze a link of m3u8
        :param url: string, the link need to analyze
        :return: list
        '''
        container = list()
        response = self.request(url).text.split('\n')
        for ts in response:
            if '.ts' in ts:
                container.append(ts)
            if '#EXT-X-KEY:' in ts:
                self.encrypt = True
        return container

    def getEncryptKey(self, url):
        '''
        Access to the secret key
        :param url: string, Access to the secret key by the url
        :return: string
        '''
        encryptKey = self.request("{}/key.key".format(url)).content
        return encryptKey

    def aesDecode(self, data, key):
        '''
        Decode the data
        :param data: stream, the data need to decode
        :param key: secret key
        :return: decode the data
        '''
        crypt = AES.new(key, AES.MODE_CBC, key)
        plain_text = crypt.decrypt(data)
        return plain_text.rstrip(b'\0')

    def download(self, queue, sort, file, downPath, url):
        '''
        Download the debris of video
        :param queue: the queue
        :param sort: which number debris
        :param file: the link of debris
        :param downPath: the path to save debris
        :param url: the link of m3u8
        :return: None
        '''
        queue.put(file)

        baseUrl = '/'.join(url.split("/")[:-1])

        if self.encrypt:
            self.encryptKey = self.getEncryptKey(baseUrl)

        if not file.startswith("http"):
            file = baseUrl + '/' +file

        debrisName = "{}/{}.ts".format(downPath, sort)

        if not os.path.exists(debrisName):
            response = self.request(file)
            with open(debrisName, "wb") as f:
                if self.encrypt:
                    data = self.aesDecode(response.content, self.encryptKey)
                    f.write(data)
                    f.flush()
                else:
                    f.write(response.content)
                    f.flush()

    def progressBar(self, queue, count):
        '''
        Show progress bar
        :param queue: the queue
        :param count: the number count of debris
        :return: None
        '''
        print('---一共{}个碎片...'.format(count))
        offset = 0
        while True:
            offset += 1
            file = queue.get()
            rate = offset * 100 / count
            print("\r%s下载成功，当前进度%0.2f%%, 第%s/%s个" % (file, rate, offset, count))
            if offset >= count:
                break

    @retry(stop_max_attempt_number=3)
    def request(self, url, params):
        '''
        Send a request
        :param url: the url of request
        :param params: the params of request
        :return: the result of request
        '''
        response = requests.get(url, params=params, headers=self.headers, timeout=10)
        assert response.status_code == 200
        return response

    def run(self):
        '''
        program entry, Input basic information
        '''
        downPath = str(input("碎片的保存路径, 默认./Download：")) or "./Download"
        savePath = str(input("视频的保存路径, 默认./Complete：")) or "./Complete"
        clearDebris = bool(input("是否清除碎片, 默认True：")) or True
        saveSuffix = str(input("视频格式, 默认ts：")) or "ts"

        while True:
            url = str(input("请输入合法的m3u8链接："))
            if self.checkUrl(url):
                break

        # create a not available folder
        if not os.path.exists(downPath):
            os.mkdir(downPath)

        if not os.path.exists(savePath):
            os.mkdir(savePath)

        # start analyze a link of m3u8
        print('---正在分析链接...')
        container = self.parse(url)
        print('---链接分析成功...')

        # run processing to do something
        print('---进程开始运行...')
        po = multiprocessing.Pool(30)
        queue = multiprocessing.Manager().Queue()
        size = 0
        for file in container:
            sort = str(size).zfill(5)
            po.apply_async(self.download, args=(queue, sort, file, downPath, url,))
            size += 1

        po.close()
        self.progressBar(queue, len(container))
        print('---进程运行结束...')

        # handler debris
        sys = platform.system()
        saveName = time.strftime("%Y%m%d_%H%M%S", time.localtime())

        print('---文件合并清除...')
        if sys == "Windows":
            os.system("copy /b {}/*.ts {}/{}.{}".format(downPath, savePath, saveName, saveSuffix))
            if clearDebris:
                os.system("rmdir /s/q {}".format(downPath))
        else:
            os.system("cat {}/*.ts>{}/{}.{}".format(downPath, savePath, saveName, saveSuffix))
            if clearDebris:
                os.system("rm -rf {}".format(downPath))
        print('---合并清除完成...')
        print('---任务下载完成...')
        print('---欢迎再次使用...')

if __name__ == "__main__":
    M3u8().hello().run()