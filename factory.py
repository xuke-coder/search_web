from queue import *
from threading import *
from time import *


class task_st:
	def __init__(self, factory, data, func):
		self.factory = factory
		self.data = data
		self.func = func
	

class task_factory(object):
	def __init__(self, max_task, max_thread):
		self.stop = False
		self.task_que = Queue(max_task)
		self.thread_pool = []
		self.init_thread_pool(max_thread)
		sleep(1)
		
	def init_thread_pool(self, max_thread):
		for i in range(max_thread):
			thr = Thread(target = self.exec_task)
			#thr.setDaemon(True)
			thr.start()
			self.thread_pool.append(thr)
		    
	def task_pop(self):
		return self.task_que.get()
	
	def task_push(self, task):
		self.task_que.put(task)
	
	def exec_task(self):
		while (not self.stop):
			task = self.task_pop()
			if (not task):
				sleep(1)
				print("...")
				continue
			
			task.func(task.factory, task.data)
	
	def stop_task(self, task):
		for thr in self.thread_pool:
			self.task_push(task)
			