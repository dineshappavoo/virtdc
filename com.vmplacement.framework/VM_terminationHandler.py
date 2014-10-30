#!/usr/bin/python
import sys, time
from multiprocessing import Process
sys.path.append('/root/Desktop/VMPlacementAndScaling/com.vmplacement.manager')
from VM_terminationList import calculate_vm_endtime
from VM_Info_Updater import getHostVMDict
from Guest import Guest
from VM_terminateGuest import vm_terminate_guest

#API to terminate the running guest in the Host

#==============================================================================
# Variables
#==============================================================================
# Some descriptive variables
#name                = "virtdc"
#version             = "0.1.0"
#long_description    = """vmplacementandscaling is a set of API's/tools written to create virtual machines for cloud users efficiently."""
#url                 = "https://github.com/dineshappavoo/VMPlacementAndScaling"
#license             = ""

#==============================================================================

#Activity Log
vmtermination_log = open('../com.vmplacement.logs/activity_logs/vmtermination.log', 'a+')


vm_termination_list = []

def fetch_vm_termination_list():
  
  while(1):
	host_vm_dict = getHostVMDict()
	for host, value in host_vm_dict.iteritems() :
		for vmid in value :
			vm_obj=value[vmid]
			vm_end_time = calculate_vm_endtime(vm_obj.vmid, vm_obj.start_time)
			if (time.time() >= vm_end_time ):
				if (vm_terminate_guest(host, vmid) ):
					vm_termination_list.append(vmid)
					vmtermination_log.write('TERMINATION HANDLER ::'+host+' :: '+vmid+' :: Guest terminated\n')
	time.sleep(20) 

def get_termination_list():
	term_list = vm_termination_list
	vm_termination_list = []
	return term_list
			

if __name__ == '__main__':
	fetch_vm_termination_list()
