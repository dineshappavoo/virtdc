#!/usr/bin/python

import time
import sys
import datetime
sys.path.append('/var/lib/virtdc/manager')
sys.path.append('/var/lib/virtdc/framework')
from VM_PlacementManager import report_usage_to_placement_manager



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
		#Activity Log
		vmlistener_log = open('/var/lib/virtdc/logs/activity_logs/vmlistener.log', 'a+')
		usage = usage.strip()
		guest_usage = usage.split('|')
		vmid = guest_usage[0].strip() if len(guest_usage[0].strip()) != 0 else 0
		cpu_usage = guest_usage[1].strip() if len(guest_usage[1].strip()) != 0 else 0
		os_mem_usage = guest_usage[2].strip() if len(guest_usage[2].strip()) != 0 else 0
		task_mem_usage = guest_usage[3].strip() if len(guest_usage[3].strip()) != 0 else 0
		io_usage = guest_usage[4].strip() if len(guest_usage[4].strip()) != 0 else 0


		path = '/var/lib/virtdc/vmonere/monitor_logs/'+vmid+'.log'
		file= open(path, 'a+')
		usage= str(datetime.datetime.now()) +' \t|\t '+ vmid+' \t|\t '+ str(cpu_usage) + '\t|\t' + str(os_mem_usage) + '\t|\t' + str(task_mem_usage) + '\t|\t' + str(io_usage)
		file.write(usage+'\n')
		file.close()


		#To report current usage to the placement manager
		report_usage_to_placement_manager(vmid, cpu_usage, task_mem_usage, io_usage)

	except Exception as e:
		vmlistener_log.write(str(datetime.datetime.now()) +' :: vmonere listener :: '+vmid+' :: error in listener / reporting to manager \n')
		vmlistener_log.write(str(e) + '\n')
		pass


if __name__ == "__main__":
	receive_guest_usage(sys.argv[1])
