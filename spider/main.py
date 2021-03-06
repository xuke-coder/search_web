import re
import sys
import gzip
import search_all
import store
import urllib


class zhihu_conf(object):
		main_url = "http://www.zhihu.com"
		login_url = "http://www.zhihu.com"
		header = {
			"Host":"www.zhihu.com",
			"User-Agent":'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
		}
		
def zhihu_login_func(opener, user_data):
	head = []
	for key, value in user_data.header.items():
		elem = (key, value)
		head.append(elem)
	
	opener.addheaders = head
	data = opener.open(user_data.login_url).read()
	try:
		data = gzip.decompress(data)
	except:
		print("not gzip file")
	finally:
		data = data.decode()
	
	exp = re.compile('name="_xsrf" value="(.*)"', flags = 0)
	list = exp.findall(data)
	
	login_url = "http://www.zhihu.com/login"
	user = "zhihu666@163.com"
	passwd = "zhihu6666"
	xsrf = list[0]
	remember = 'y'
	
	post_data = {
		'email':user,
		'_xsrf':xsrf,
		'password':passwd,
		'rememberme':remember
	}
	
	print (post_data)
	post_data = urllib.parse.urlencode(post_data).encode()
	data = opener.open(login_url, post_data).read()
	try:
		data = gzip.decompress(data)
	except:
		print("not gzip file")
	finally:
		data = data.decode()
	return data

def zhihu_search_func():
	print("search..")

def zhihu_request_func(link, opener, user_data):
	link = user_data.main_url + "/" + link
	print("read link %s" % link)
	try:
		data = opener.open(link).read()
	except:
		print("read nothing!!!")
		return
		
	try:
		data = gzip.decompress(data)
		return data.decode()
	except:
		pass
	return data
	

if __name__=="__main__":
	wconf = search_all.web_conf()
	wconf.user_data = zhihu_conf()
	wconf.user_login_func = zhihu_login_func
	wconf.user_search_func = zhihu_search_func
	wconf.user_request_func = zhihu_request_func
	wconf.deep_num = 10
	wconf.wide_num = 100
	
	sconf = store.store_conf()
	sconf.level_num = 2
	sconf.every_level_num = 10
	sconf.store_path = "/mnt/nfs/path_base"
	
	wsearch = search_all.search_one_web(wconf, sconf)
	wsearch.run("")
