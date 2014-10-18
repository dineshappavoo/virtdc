#!/usr/local/bin/python

# usage example: python parse.py -T 20
# cat 20.csv

import optparse
import sys
import math
import csv

parser = optparse.OptionParser()

parser.add_option("-t", "--task-usage", dest="task", help="task usage source file", action="store", default="task_usage-part-00000-of-00500_small.csv")

parser.add_option("-T", "--task-index", dest="task_index", help="task usage source file", action="store")

(options, args) = parser.parse_args()

# 1,start time,INTEGER,YES
# 2,end time,INTEGER,YES
# 4,task index,INTEGER,YES
# 6,CPU rate,FLOAT,NO
# 8,assigned memory usage,FLOAT,NO
# 9,unmapped page cache,FLOAT,NO
# 10,total page cache,FLOAT,NO
# 11,maximum memory usage,FLOAT,NO
# 12,disk I/O time,FLOAT,NO
# 13,local disk space usage,FLOAT,NO
# 14,maximum CPU rate,FLOAT,NO
# 15,maximum disk IO time,FLOAT,NO

# group by task_index

all_tasks = {}

with open(options.task, 'rb') as csvfile:
	task_reader = csv.reader(csvfile, delimiter=',')
	for row in task_reader:
		task_index = row[3]
		start_time = row[0]
		end_time = row[1]
		cpu_rate = row[5]
		memory = round(float(row[6]), 2) * 500000   # in Kb
		io_usage = round(float(row[11]), 2)
		data = ((int(end_time) - int(start_time)) / 1000000, round(float(cpu_rate), 2), memory, io_usage)
		if(task_index not in all_tasks):
			all_tasks[task_index] = [data]
		else:
			all_tasks[task_index].append(data)
			
if(options.task_index and options.task_index in all_tasks):
	with open("VM_Task_" + options.task_index + '.csv', 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=' ')
		max_cpu = 1
		max_memory = 0
		for n in all_tasks[task_index]:
			curr_load = n[1]
			curr_memory = n[2]
			if(math.ceil(curr_load) > max_cpu):
				max_cpu = int(math.ceil(curr_load))
			if(math.ceil(curr_memory) > max_memory):
				max_memory = int(math.ceil(curr_memory))
			writer.writerow(n)
		writer.writerow([max_cpu])
		writer.writerow([max_memory])






