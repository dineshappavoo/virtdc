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

	usage = usage.strip()
	guest_usage = usage.split()
	vmid = guest_usage[0]
	cpu_usage = guest_usage[2]
	os_mem_usage = guest_usage[4]
	task_mem_usage = guest_usage[6]
	io_usage = guest_usage[8]

        file= open('/var/lib/virtdc/com.vmplacement.logs/monitor_logs/vmusageTest.log', 'a+')
	usage= vmid+' \t|\t '+ str(cpu_usage) + '\t|\t' + str(os_mem_usage) + '\t|\t' + str(task_mem_usage) + '\t|\t' + str(io_usage) +"\n"
        file.write(usage+'\n')
	#print usage


if __name__ == "__main__":
	receive_guest_usage(sys.argv[1])
