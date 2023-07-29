#!/usr/bin/env python
# encoding: utf-8
'''
#-------------------------------------------------------------------
#                   CONFIDENTIAL --- CUSTOM STUDIOS
#-------------------------------------------------------------------
#
#                   @Project Name : 下载《笔趣看》网小说
#
#                   @File Name    : biqukan.py
#
#                   @Programmer   : tinygeeker
#
#                   @Start Date   : 2022/01/10 13:14
#
#                   @Last Update  : 2022/01/10 13:14
#
#-------------------------------------------------------------------
'''
from urllib import request
from bs4 import BeautifulSoup
import collections, re, os, sys

class biqukan:
	'''
	 This is a main Class, the file contains all documents.
	 One document contains paragraphs that have several sentences
	 It loads the original file and converts the original file to new content
	 Then the new content will be saved by this class
	'''
	def __init__(self):
		self.header = {
			'User-Agent': 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
		}

	def hello(self):
		'''
        This is a welcome speech
        :return: self
        '''
		print('*' * 50)
		print(' ' * 15 + '下载《笔趣看》网小说')
		print(' ' * 5 + '作者: tinygeeker  Date: 2022-01-10 13:14')
		print(' ' * 5 + '主页: https://tinygeeker.blog.csdn.net')
		print('*' * 50)
		return self

	def get_download_url(self, target_url):
		'''
		get download url
		'''
		charter = re.compile(u'[第弟](.+)章', re.IGNORECASE)
		target_req = request.Request(url = target_url, headers = self.header)
		target_response = request.urlopen(target_req)
		target_html = target_response.read().decode('gbk','ignore')
		list_main_soup = BeautifulSoup(target_html,'lxml')
		chapters = list_main_soup.find_all('div',class_ = 'listmain')
		download_soup = BeautifulSoup(str(chapters), 'lxml')
		novel_name = str(download_soup.dl.dt).split("》")[0][5:]
		flag_name = "《" + novel_name + "》" + "正文卷"
		numbers = (len(download_soup.dl.contents) - 1) / 2 - 8
		download_dict = collections.OrderedDict()
		begin_flag = False
		numbers = 1
		for child in download_soup.dl.children:
			if child != '\n':
				if child.string == u"%s" % flag_name:
					begin_flag = True
				if begin_flag == True and child.a != None:
					download_url = "https://www.biqukan.com" + child.a.get('href')
					download_name = child.string
					names = str(download_name).split('章')
					name = charter.findall(names[0] + '章')
					if name:
							download_dict['第' + str(numbers) + '章 ' + names[1]] = download_url
							numbers += 1
		return novel_name + '.txt', numbers, download_dict

	def downloader(self, url):
		'''
		download the text
		'''
		download_req = request.Request(url = url, headers = self.header)
		download_response = request.urlopen(download_req)
		download_html = download_response.read().decode('gbk','ignore')
		soup_texts = BeautifulSoup(download_html, 'lxml')
		texts = soup_texts.find_all(id = 'content', class_ = 'showtxt')
		soup_text = BeautifulSoup(str(texts), 'lxml').div.text.replace('\xa0','')
		return soup_text

	def writer(self, name, path, text):
		'''
		write to file
		'''
		write_flag = True
		with open(path, 'a', encoding='utf-8') as f:
			f.write(name + '\n\n')
			for each in text:
				if each == 'h':
					write_flag = False
				if write_flag == True and each != ' ':
					f.write(each)
				if write_flag == True and each == '\r':
					f.write('\n')
			f.write('\n\n')

	def run(self):
		'''
		program entry
		'''
		target_url = str(input("请输入小说目录下载地址:\n"))

		# 实例化下载类
		d = self.downloader(target_url)
		name, numbers, url_dict = d.get_download_url(target_url)
		if name in os.listdir():
			os.remove(name)
		index = 1

		# 下载中
		print("《%s》下载中:" % name[:-4])
		for key, value in url_dict.items():
			d.Writer(key, name, d.Downloader(value))
			sys.stdout.write("已下载:%.3f%%" % float(index / numbers) + '\r')
			sys.stdout.flush()
			index += 1

		print("《%s》下载完成！" % name[:-4])


if __name__ == '__main__':
	biqukan().hello().run()

	
