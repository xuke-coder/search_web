import urllib
import http.cookiejar
import re
import store
import threading
from factory import *

class user_box(object):
	def __init__(self, deep, page_link, page_data):
		self.deep = deep
		self.page_link = page_link
		self.page_data = page_data
		
class web_conf(object):
	def __init__(self):
		self.user_data = ""
		self.user_login_func = ""
		self.user_search_func = ""
		self.deep_num = ""
		self.wide_num = ""

class search_one_web(object):
	def __init__(self, web_conf, store_conf):
		self.link_list = []
		self.web_conf = web_conf
		self.store = store.store_mgr(store_conf)
		self.create_opener()
		self.factory = task_factory(10240, 20)
		self.mutex = threading.Lock()
		
	def create_opener(self):
		http_cookie_procsser = urllib.request.HTTPCookieProcessor()
		self.opener = urllib.request.build_opener(http_cookie_procsser)
		
	def login(self):
		return self.web_conf.user_login_func(self.opener, self.web_conf.user_data)
	
	def find_link_from_page(self, page_link, page_data):
		if 0: #线程版
			#制造task
			ubox = user_box(self.web_conf.deep_num, page_link, page_data)
			task = task_st(self.factory, ubox, self.spider)
			self.factory.task_push(task)
		else:
			self.spider(self.web_conf.deep_num, page_link, page_data)
		
	#def spider(self, factory, data):
	def spider(self, deep, page_link, page_data):
		if 0:#线程版
			page_link = data.page_link
			page_data = data.page_data
			deep = data.deep
		
		if (page_link in self.link_list):
			return
		
		if 0:#线程版
			#对链接列表加锁
			self.mutex.acquire()
			self.link_list.append(page_link)
			self.mutex.release()
		else:
			self.link_list.append(page_link)
		
		print("store")
		self.store.store_file(page_link, page_data)
		
		if deep <= 0:
			return
			
		exp = re.compile('href="/([a-z0-9A-Z_\-\/.%]+)"', flags = 0)
			
		try:
			list = exp.findall(page_data)
		except:
			page_data = page_data.decode()
			list = exp.findall(page_data)
			
		for link_page in list:
			if (link_page[-4:] == ".gif" or link_page[-4:] == ".css" or link_page[-4:] == ".png"
				or link_page[-3:] == ".js"):
				continue
			
			if (link_page in self.link_list):
				continue
			
			data = self.web_conf.user_request_func(link_page, self.opener, self.web_conf.user_data)
			
			if 0:#线程版
				#制造task
				ubox = user_box(deep - 1, link_page, data)
				task = task_st(factory, ubox, self.spider)
				factory.task_push(task)
			else:
				self.spider(deep - 1, link_page, data)
			
			
		
	def run(self, main_link):
		main_page_data = self.login()
		self.find_link_from_page(main_link, main_page_data)
		
