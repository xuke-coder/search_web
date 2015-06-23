#!/usr/bin/python

from  factory import *

class A:
	def __init__(self, factory):
		self.factory = factory
		
	def ufunc(self, factory, data):
		print(data)
		if (data == "stop"):
			factory.stop = True
		
	
if __name__ == "__main__":
	factory = task_factory(1024, 10)
	a = A(factory)
	task1 = task_st(factory, "one", a.ufunc)
	task2 = task_st(factory, "two", a.ufunc)
	factory.task_push(task1)
	factory.task_push(task2)
	sleep(1)
	task3 = task_st(factory, "stop", a.ufunc)
	factory.stop_task(task3)
	
