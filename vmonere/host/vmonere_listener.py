#!/usr/bin/python

import time
import sys
import datetime
sys.path.append('/var/lib/virtdc/manager')
sys.path.append('/var/lib/virtdc/framework')
from VM_PlacementManager import process_action_on_current_usage
from virtdc_command_line_utility import get_host_name, get_domain_object


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

		#To report current usage to the placement manager
		report_usage_to_placement_manager(vmid, cpu_usage, mem_usage, io_usage)

	except Exception as e:
		pass
	

	path = '/var/lib/virtdc/logs/monitor_logs/'+vmid+'.log'
        file= open(path, 'a+')
	usage= str(datetime.datetime.now()) +' \t|\t '+ vmid+' \t|\t '+ str(cpu_usage) + '\t|\t' + str(os_mem_usage) + '\t|\t' + str(task_mem_usage) + '\t|\t' + str(io_usage) +"\n"
        file.write(usage+'\n')
	file.close()


def report_usage_to_placement_manager(vmid, cpu_usage, mem_usage, io_usage):

	try:
		host = get_host_name(vmid)
		domain_object = get_domain_object(vmid)
		process_action_on_current_usage(host, vmid, domain_object, cpu_usage, mem_usage, io_usage)	

	except Exception as e:
		pass
	

if __name__ == "__main__":
	receive_guest_usage(sys.argv[1])
