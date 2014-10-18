#!/usr/bin/python
#
import optparse
import threading
import subprocess
from timeout import timeout

parser = optparse.OptionParser()
parser.add_option("-T", "--task-set", dest="task", help="task input file", action="store", default="./task.dat")

(options, args) = parser.parse_args()

stop_command = '''
for n in `cat ~/io.pid`; do kill -STOP $n; done
'''

cont_command = '''
for n in `cat ~/io.pid`; do kill -CONT $n; done
'''

# a 30-element list.
# each element stands for disk util for certain 2 seconds within the last 60 seconds
util_last_min = [0] * 30

def populateUtilList():
    i = 0
    while(True):
        command = "/usr/bin/iostat -d -x 1 2 | grep sda | tail -1 | awk '{print $14}'"
        util_value = float(subprocess.check_output(command, shell=True))/100  # percentage to value
        util_last_min[i % 30] = util_value
        i += 1

def getDiskUtil():
    return sum(util_last_min, 0.0) / len(util_last_min)


def run(command):
    return subprocess.check_output(command, shell=True)

def wrapTimeOut(target, time):
	@timeout(time)
	def func(target):
		while(True):
			util = getDiskUtil()
			if(util < target):
				print "Disk util(%s) lower than target, iostress.sh will be running." % util
				go = run(cont_command)
			elif(util > target):
				print "Disk util(%s) higher than target, iostress.sh will be stopped." % util
				go = run(stop_command)
			sleep(2)
	return func

    
# start a thread to maintain the last minute disk util list
t = threading.Thread(target=populateUtilList, args = ())
t.daemon = True
t.start()

all_tasks = []
try:
    with open(options.task, 'r') as f:
        for line in f:
            lines = line[:-2].split(' ')
            if(len(lines) >= 2):
                all_tasks.append([(int(lines[0]), float(lines[2])) for line in f])
except Exception as e:
    print e

for l in all_tasks:
    if(len(l) < 2):
        continue
    target = l[1]
    time = l[0]
    try:
        curr_func = wrapTimeOut(target, time)
        curr_func(target)
    except:
        continue
