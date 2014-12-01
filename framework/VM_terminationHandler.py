#!/usr/bin/python

import sys, time
import datetime
from multiprocessing import Process
sys.path.append('/var/lib/virtdc/manager')
from VM_calculateLifeTime import calculate_vm_endtime
from VM_Info_Updater import getHostVMDict
from Guest import Guest
from VM_terminateGuest import vm_terminate_guest

#API to terminate the running guest in the Host after calculating the life time

#==============================================================================
# Variables
#==============================================================================

# Some descriptive variables
#name                = "virtdc"
#version             = "0.1.0"
#long_description    = """virtdc is a set of API's/tools written to create virtual machines for cloud users efficiently."""
#url                 = "https://github.com/dineshappavoo/virtdc"
#license             = ""

#==============================================================================

#Activity Log
vmtermination_log = open('/var/lib/virtdc/logs/activity_logs/vmtermination.log', 'a+')


vm_termination_list = []

def find_lifetime_and_terminate_vm():
  print 'termination'
  while(1):
	host_vm_dict = getHostVMDict()

	for node, vm_dict in host_vm_dict.iteritems():
        	for vmid,value in vm_dict.iteritems():
			vm_end_time = calculate_vm_endtime(value.vmid, value.start_time)

			#print vm_end_time
			#For Testing purpose we are subtracting 9000 seconds
			vm_end_time = float(vm_end_time) - float(9100)
			print 'VMID '+vmid+' Host '+node+' Current Time  : '+ str(int(time.time()/60)) +' End Time : '+str(int(vm_end_time/60))
			if (time.time() >= vm_end_time ):
				if (vm_terminate_guest(node, vmid) ):
					vm_termination_list.append(vmid)
					vmtermination_log.write(str(datetime.datetime.now()) +' :: TERMINATION HANDLER ::'+node+' :: '+vmid+' :: Guest terminated\n')
					
	time.sleep(20) 

def get_termination_list():
	term_list = vm_termination_list
	vm_termination_list = []
	return term_list
			

if __name__ == '__main__':
	find_lifetime_and_terminate_vm()

