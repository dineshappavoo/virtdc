#!/usr/bin/python
######################################################
# this is a prototype for cpu stress only.
# We need to expend it to accomodate men and io stress
######################################################
import optparse
import sys
import subprocess
from timeout import timeout
from time import sleep
import os
import random

parser = optparse.OptionParser()

parser.add_option("-T", "--task-set", dest="task", help="task input file", action="store", default="./task.dat")

(options, args) = parser.parse_args()

#stress_command = '''150000
#stress -t 1h -c 3 --vm-bytes 64m &
#'''

uptime_command = "cat /proc/loadavg | awk '{print $1}'"

memory_command = '''
cat /proc/`cat /root/memory.pid`/status | grep VmSize | awk '{print $2}'
'''

memory_init_command = '''
nice -n 19 /root/StressMemory %s &
echo $! > /root/memory.pid
'''
memory_clear_command = '''
for n in `cat /root/memory.pid`
do
kill -9 $n || true
done
'''

memory_stop_command = '''
for n in `cat /root/memory.pid`; do kill -STOP $n || true; done
'''

memory_cont_command = '''
for n in `cat /root/memory.pid`; do kill -CONT $n || true; done
'''

stop_command = '''
for n in `cat /root/cpu.pid`; do kill -STOP $n || true; done
'''

cont_command = '''
for n in `cat /root/cpu.pid`; do kill -CONT $n || true; done
'''

run_cpusim = '''
/root/cpuSim %s %s
'''

reboot_command = '''
reboot
'''

def getUptime(uptime_output):
	# Return a float to represent uptime
	return float(uptime_output.strip())

def getMemory(memory_output):
	# Return an integer to represent memory
	return int(memory_output.strip())

def run(command):
	return subprocess.check_output(command, shell=True)

def wrapTimeOut(target, time, memory):
	@timeout(time)
	def func(target, memory):
		clear_memory = run(memory_clear_command)
		os.system(memory_init_command % memory)
		cpuSim = run(run_cpusim % (target, time))
		sleep(500)
#		while(True):
#			up = getUptime(run(uptime_command))
##			memory_used = getMemory(run(memory_command)) - 150000
#			if(up < target):
#				print "The uptime now is %s, cpu program will be running." % up
#				go = run(cont_command)
#			elif(up > target):
#				print "The uptime now is %s, cpu program will not be running." % up
#				go = run(stop_command)
#			if(memory_used < memory):
#				print 'The total memory used now is %s, memory program will be running.' % memory_used
#				go = run(memory_cont_command)
#			elif(memory_used > memory):
#				print 'The total memory used now is %s, memory program will be running.' % memory_used
#				go = run(memory_stop_command)

#			sleep(2)
	return func


all_tasks = []
try:
        with open(options.task, 'r') as f:
		for line in f:
			lines = line[:-2].split(' ')
			if(len(lines) >= 2):
                		all_tasks = all_tasks + [(int(lines[0]), float(lines[1]), float(lines[2]))]
except Exception as e:
	print e

for l in all_tasks:
	if(len(l) < 2):
		continue
	target = l[1]
	time = l[0]
	memory = l[2]
	try:
		lucky_num = round(random.random(), 2)
		if(lucky_num == 0.01):
			reboot = run(reboot_command)
		curr_func = wrapTimeOut(target, time, memory)
		curr_func(target, memory)
	except Exception as e:
		print 'Exception is, ', e
		continue
	
	
