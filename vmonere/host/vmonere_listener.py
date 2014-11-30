#!/usr/bin/python

import time
import sys

#==============================================================================
# Variables
#==============================================================================
# Some descriptive variables
#name                = "virtdc"
#version             = "0.1.0"
#long_description    = """vmplacementandscaling is a set of API's/tools written to create virtual machines for cloud users efficiently."""
#url                 = "https://github.com/dineshappavoo/virtdc"
#license             = ""

#==============================================================================

def receive_guest_usage(usage):
	
	#print 'Listener '+str(usage)
	try:
		usage = usage.strip()
		guest_usage = usage.split('|')
		vmid = guest_usage[0].strip() if len(guest_usage[0].strip()) != 0 else 0
		cpu_usage = guest_usage[1].strip() if len(guest_usage[1].strip()) != 0 else 0
		os_mem_usage = guest_usage[2].strip() if len(guest_usage[2].strip()) != 0 else 0
		task_mem_usage = guest_usage[3].strip() if len(guest_usage[3].strip()) != 0 else 0
		io_usage = guest_usage[4].strip() if len(guest_usage[4].strip()) != 0 else 0


	except Exception as e:
		pass
	

	path = '/var/lib/virtdc/logs/monitor_logs/'+vmid+'.log'
        file= open(path, 'a+')
	usage= vmid+' \t|\t '+ str(cpu_usage) + '\t|\t' + str(os_mem_usage) + '\t|\t' + str(task_mem_usage) + '\t|\t' + str(io_usage) +"\n"
        file.write(usage+'\n')
	file.close()


if __name__ == "__main__":
	receive_guest_usage(sys.argv[1])
