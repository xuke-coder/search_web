import os
import string
import hashlib
import gzip
import re
import sys


class store_conf(object):
	def __init__(self):
		self.level_num = ""
		self.every_level_num = ""
		self.store_path = ""
		
	
class store_mgr(object):
	def __init__(self, conf):
		self.conf = conf
		self.make_dir(self.conf.store_path, self.conf.level_num, self.conf.every_level_num)

	def make_dir(self, base_path, level_num, every_level_num):
		if (level_num > 0):
			for i in range(every_level_num):
				path = base_path + "/" + str(i)
				os.system("mkdir -p " + path)
				#print path
				self.make_dir(path, level_num - 1, every_level_num)
		
		
	def get_file_path(self, path, file_md5, level_num, every_level_num):
		if (level_num > 0):
			path = path + "/" + str(int(file_md5, 16) % every_level_num)
			return self.get_file_path(path, str(int(file_md5, base=16) // every_level_num), level_num - 1, every_level_num)
		
		return path
	
	def store_file(self, file_name, data):
		md5_obj = hashlib.md5()
		#print(file_name)
		md5_obj.update(file_name.encode())
		file_md5 = md5_obj.hexdigest()
		#print(file_md5)
		path = self.get_file_path(self.conf.store_path, file_md5, self.conf.level_num, self.conf.every_level_num) + "/" + str(file_md5)
		print("store path = %s" % path)
		self.write_file(path, data, file_name)
	
	def write_file(self, file_path, data, link_path):
		if (type(data) == type("aa")):
			file = open(file_path, "w")
			data = link_path + "\n" + data
		else:
			file = open(file_path, "w")
			data = data.decode('utf8')
			data = link_path + "\n" + data
			
		try:
			
			file.write(data)
		except:
			print("write file %s error" % file_path)
		finally:
			file.close()
		
if __name__ == "__main__":
	conf = store_conf()
	conf.level_num = 2
	conf.every_level_num = 10
	conf.store_path = "/mnt/nfs/path_one"
	
	store = store_mgr(conf)
	store.store_file("one_two", "good")