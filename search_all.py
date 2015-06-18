import urllib
import http.cookiejar
import re
import store

class web_conf(object):
	def __init__(self):
		self.user_data = ""
		self.user_login_func = ""
		self.user_search_func = ""
		self.deep_num = ""
		self.wide_num = ""

class search_one_web(object):
	def __init__(self, web_conf, store_conf):
		self.web_conf = web_conf
		self.store = store.store_mgr(store_conf)
		self.create_opener()
		
	def create_opener(self):
		http_cookie_procsser = urllib.request.HTTPCookieProcessor()
		self.opener = urllib.request.build_opener(http_cookie_procsser)
		
	def login(self):
		return self.web_conf.user_login_func(self.opener, self.web_conf.user_data)
	
	def find_link_from_page(self, page_link, page_data):
		#self.store.store_file(page_link, page_data)
		#self.web_conf.user_search_func()
		self.spider(self.web_conf.deep_num, page_link, page_data)
		
	def spider(self, deep, page_link, page_data):
		self.store.store_file(page_link, page_data)
		if deep > 0:
			exp = re.compile('href="/([a-z0-9A-Z_\-\/.%]+)"', flags = 0)
			list = exp.findall(page_data)
			for link_page in list:
				data = self.web_conf.user_request_func(link_page, self.opener, self.web_conf.user_data)
				self.spider(deep - 1, link_page, data)
		
	def run(self, main_link):
		main_page_data = self.login()
		self.find_link_from_page(main_link, main_page_data)
		
