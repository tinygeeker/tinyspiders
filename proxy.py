#!/usr/bin/env python
# encoding: utf-8
'''
#-------------------------------------------------------------------
#                   CONFIDENTIAL --- CUSTOM STUDIOS
#-------------------------------------------------------------------
#
#                   @Project Name : 获取可用代理助手
#
#                   @File Name    : main.py
#
#                   @Programmer   : autofelix
#
#                   @Start Date   : 2022/01/09 13:14
#
#                   @Last Update  : 2022/01/09 13:14
#
#-------------------------------------------------------------------
'''
from bs4 import BeautifulSoup
import subprocess as sp
from lxml import etree
import re, random, requests

class proxy:
	def __init__(self):
		'''
		 This is a main Class, the file contains all documents.
		 One document contains paragraphs that have several sentences
		 It loads the original file and converts the original file to new content
		 Then the new content will be saved by this class
		'''
		self.target_url = 'https://www.kuaidaili.com/free/inha/%s'
		self.target_headers = {
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Referer': 'https://www.kuaidaili.com',
			'Accept-Encoding': 'gzip, deflate, sdch',
			'Accept-Language': 'zh-CN,zh;q=0.8',
		}

	def hello(self):
		'''
        This is a welcome speech
        :return: self
        '''
		print('*' * 50)
		print(' ' * 20 + '获取可用代理助手')
		print(' ' * 5 + '作者: autofelix  Date: 2022-01-09 13:14')
		print(' ' * 5 + '主页: https://autofelix.blog.csdn.net')
		print('*' * 50)
		return self

	def run(self):
		'''
		program entry
		'''
		lose_time, waste_time = self.initpattern()
		proxy_list = self.get_proxy(1)

		# 如果平均时间超过200ms重新选取ip
		while True:
			# 从100个IP中随机选取一个IP作为代理进行访问
			proxy = random.choice(proxy_list)
			split_proxy = proxy.split('#')
			# 获取IP
			ip = split_proxy[1]
			# 检查ip
			average_time = self.check_ip(ip, lose_time, waste_time)
			if average_time > 200:
				# 去掉不能使用的IP
				proxy_list.remove(proxy)
				print('ip:{}丢包, 重新获取中!' . format(ip))
			if average_time < 200:
				break

		proxy_list.remove(proxy)
		proxy_dict = {split_proxy[0]: split_proxy[1] + ':' + split_proxy[2]}
		print('可用代理：', proxy_dict)

	def get_proxy(self, page=1):
		S = requests.Session()
		target_url = self.target_url % page
		# get请求
		target_response = S.get(url=target_url, headers=self.target_headers)
		# utf-8编码
		target_response.encoding = 'utf-8'
		# 获取网页信息
		target_html = target_response.text
		# 获取id为ip_list的table
		bf1_ip_list = BeautifulSoup(target_html, 'lxml')
		ip_list_info = bf1_ip_list.find(id='list').find_all('tr')
		# 存储代理的列表
		proxy_list = []
		# 爬取每个代理信息
		for index in range(len(ip_list_info)):
			if index > 0:
				dom = etree.HTML(str(ip_list_info[index]))
				ip = dom.xpath('//td[1]')
				port = dom.xpath('//td[2]')
				protocol = dom.xpath('//td[4]')
				proxy_list.append(protocol[0].text.lower() + '#' + ip[0].text + '#' + port[0].text)
		# 返回代理列表
		return proxy_list

	def check_ip(self, ip, lose_time, waste_time):
		'''
		Detect whether the agent is available
		:param ip: ip
		:param lose_time: lose_time
		:param waste_time: waste_time
		:return: int
		'''
		# 命令 -n 要发送的回显请求数 -w 等待每次回复的超时时间(毫秒)
		cmd = "ping -n 3 -w 3 %s"
		# 执行命令
		p = sp.Popen(cmd % ip, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
		# 获得返回结果并解码
		out = p.stdout.read().decode("gbk")
		# 丢包数
		lose_time = lose_time.findall(out)
		# 当匹配到丢失包信息失败,默认为三次请求全部丢包,丢包数lose赋值为3
		if len(lose_time) == 0:
			lose = 3
		else:
			lose = int(lose_time[0])
		# 如果丢包数目大于2个,则认为连接超时,返回平均耗时1000ms
		if lose > 2:
			# 返回False
			return 1000
		# 如果丢包数目小于等于2个,获取平均耗时的时间
		else:
			# 平均时间
			average = waste_time.findall(out)
			# 当匹配耗时时间信息失败,默认三次请求严重超时,返回平均好使1000ms
			if len(average) == 0:
				return 1000
			else:
				average_time = int(average[0])
				# 返回平均耗时
				return average_time

	def initpattern(self):
		'''
		Regular matching
		'''
		lose_time = re.compile(u"丢失 = (\d+)", re.IGNORECASE)
		waste_time = re.compile(u"平均 = (\d+)ms", re.IGNORECASE)
		return lose_time, waste_time

if __name__ == '__main__':
	proxy().hello().run()
