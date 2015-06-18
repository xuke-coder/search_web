#!/usr/bin/python

from  factory import *

def user_func(factory, data):
	print(data)
	if (data == "stop"):
		factory.stop = True
	
	
if __name__ == "__main__":
	factory = task_factory(1024, 10)
	task1 = task_st(factory, "one", user_func)
	task2 = task_st(factory, "two", user_func)
	factory.task_push(task1)
	factory.task_push(task2)
	sleep(1)
	task3 = task_st(factory, "stop", user_func)
	factory.stop_task(task3)
	
