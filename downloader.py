#!/usr/bin/env python
# encoding: utf-8
'''
#-------------------------------------------------------------------
#                   CONFIDENTIAL --- CUSTOM STUDIOS
#-------------------------------------------------------------------
#
#                   @Project Name : 文件下载小助手
#
#                   @File Name    : downloader.py
#
#                   @Programmer   : autofelix
#
#                   @Start Date   : 2022/01/09 13:14
#
#                   @Last Update  : 2022/01/09 13:14
#
#-------------------------------------------------------------------
'''
import requests  
from contextlib import closing

class ProgressBar(object):
    '''
     This is a main Class, the file contains all documents.
     One document contains paragraphs that have several sentences
     It loads the original file and converts the original file to new content
     Then the new content will be saved by this class
    '''
    def __init__(self, title, count=0.0, run_status=None, fin_status=None, total=100.0, unit='', sep='/', chunk_size=1.0):  
        super(ProgressBar, self).__init__()  
        self.info = "[%s] %s %.2f %s %s %.2f %s"  
        self.title = title  
        self.total = total  
        self.count = count  
        self.chunk_size = chunk_size  
        self.status = run_status or ""  
        self.fin_status = fin_status or " " * len(self.status)  
        self.unit = unit  
        self.seq = sep  
  
    def __get_info(self):  
        '''
        [名称] 状态 进度 单位 分割线 总数 单位
        '''
        _info = self.info % (self.title, self.status, self.count/self.chunk_size, self.unit, self.seq, self.total/self.chunk_size, self.unit)  
        return _info  
  
    def refresh(self, count = 1, status = None):
        '''
        Refresh the progress
        '''
        self.count += count  
        self.status = status or self.status  
        end_str = "\r"  
        if self.count >= self.total:  
            end_str = '\n'  
            self.status = status or self.fin_status  
        print(self.__get_info(), end=end_str, )


if __name__ == '__main__':
    print('*' * 50)
    print(' ' * 20 + '文件下载小助手')
    print(' ' * 5 + '作者: autofelix  Date: 2022-01-09 13:14')
    print(' ' * 5 + '主页: https://autofelix.blog.csdn.net')
    print('*' * 50)
    url  = input('请输入需要下载的文件链接:\n')
    filename = url.split('/')[-1]
    with closing(requests.get(url, stream=True)) as response:
        chunk_size = 1024
        content_size = int(response.headers['content-length'])
        if response.status_code == 200:
            print('文件大小:%0.2f KB' % (content_size / chunk_size))
            progress = ProgressBar("%s下载进度" % filename
			            , total = content_size  
			            , unit = "KB"  
			            , chunk_size = chunk_size  
			            , run_status = "正在下载"  
			            , fin_status = "下载完成")  

            with open(filename, "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    progress.refresh(count=len(data))
        else:
            print('链接异常')