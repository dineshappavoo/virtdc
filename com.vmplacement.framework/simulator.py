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

parser = optparse.OptionParser()

parser.add_option("-T", "--task-set", dest="task", help="task input file", action="store", default="./task.dat")

(options, args) = parser.parse_args()

stress_command = '''
stress -t 1h -c 3 --vm-bytes 64m &
'''

uptime_command = '''
uptime | cut -d':' -f5 | cut -d',' -f1
'''

stop_command = '''
for n in `ps -A | grep stress | cut -f1 -d' '`; do kill -STOP $n; done
'''

cont_command = '''
for n in `ps -A | grep stress | cut -f1 -d' '`; do kill -CONT $n; done
'''

def getUptime(uptime_output):
	# Return a float to represent uptime
	return float(uptime_output[:5].strip())

def run(command):
	return subprocess.check_output(command, shell=True)

def wrapTimeOut(target, time):
	@timeout(time)
	def func(target):
		while(True):
			up = getUptime(run(uptime_command))
			if(up < target):
				print "The uptime now is %s, stress will be running." % up
				go = run(cont_command)
			elif(up > target):
				print "The uptime now is %s, stress will be stopped." % up
				go = run(stop_command)
			sleep(2)
	return func


all_tasks = []
try:
        with open(options.task, 'r') as f:
                all_tasks = all_tasks + [(int(line.split(' ')[0]), float(line.split(' ')[1])) for line in f]
except:
	print 'Cannot open task.dat file.'
	sys.exit(1)
for l in all_tasks:
	target = l[1]
	time = l[0]
	try:
		curr_func = wrapTimeOut(target, time)
		curr_func(target)
	except:
		continue
	
	
