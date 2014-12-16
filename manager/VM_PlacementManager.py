#!/usr/bin/python

import sys, time, math
import datetime
sys.path.append('/var/lib/virtdc/framework')
from VM_Info_Updater import addOrUpdateDictionaryOfVM
from Guest import Guest
from VM_migrateGuest import vm_migrate_guest
from VM_cpuScaling import vm_cpu_scaling
from VM_memoryScaling import vm_memory_scaling, vm_max_memory_scaling
from VM_decisionMaker import NodeFinder
from virtdc_command_line_utility import get_host_name, get_domain_object

from Host_Info_Tracker import GetNodeDict


#API for VM placement manager
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
#Global variables

#Memory threshold values
mem_scale_up_threshold = '10240'	# 10 MB
mem_scale_down_threshold = '102400' 	# 100 MB
time_threshold = '300' 			# 5 minutes
_base_mem_size = 2097152       		# 2 GB (This includes OS memory)



def initiateLiveMigration(vmid,sourcenode,destnode):
	a=0


#Not used
def makeMemScalingDecision(hostName,guest,memoryUsage,time):
	memoryAlloted=guest.current_memory
	maxMemory=''
#	if(memoryUsage>memoryAlloted):
#		if(memoryUsage<maxMemory):
#			initiateMemScaleUpOrDown(hostName, guest.vmid, memoryUsage)
#		else:
#			requiredExtraMemory=float(memoryUsage)-float(maxMemory)
#			if(requiredExtraMemory>memScaleUpThreshold):
				#report user through email
				#if needed do a memory scale up and charge more based on SLA
#			else:
#				initiateMemScaleUpOrDown(hostName, guest.vmid, memoryUsage)

def report_usage_to_placement_manager(vmid, cpu_usage, mem_usage, io_usage):

	try:
		host = get_host_name(vmid)
		domain_object = get_domain_object(vmid)
		print domain_object
		process_action_on_current_usage(host, vmid, domain_object, float(cpu_usage), float(mem_usage), float(io_usage))	

	except Exception as e:
		print e


#Process current usage and take action based on SLA
def process_action_on_current_usage(host, vmid, value, cpu_usage, mem_usage, io_usage):

	node_dict = GetNodeDict()

	#for key, value in node_dict.iteritems() :
	    #print key, value.hostname, value.ip_address, value.max_cpu, value.max_memory, value.max_io, value.avail_cpu, value.avail_memory, value.avail_io

	#Log activity
	manager_activity_log = open('/var/lib/virtdc/logs/activity_logs/manager.log', 'a+')

	manager_activity_log.write(str(datetime.datetime.now())+'::PLACEMENT MANAGER::MEMORY::'+host+' :: '+vmid+' :: Alotted Memory '+str(value.current_memory)+' :: Current Memory '+str(mem_usage)+'\n')
	manager_activity_log.write(str(datetime.datetime.now())+'::PLACEMENT MANAGER::CPU::'+host+' :: '+vmid+' :: Alotted CPU '+str(value.current_cpu)+' :: Current CPU '+str(cpu_usage)+'\n')

	obj=NodeFinder()
	max_cpu = value.max_cpu
	print 'Max CPU '+str(max_cpu)
	allotted_cpu = float(value.current_cpu)
	print allotted_cpu

	#Base OS should not go below the minimum memory
	mem_usage = float(mem_usage) + float(_base_mem_size)

	allotted_memory = float(value.current_memory)


	#allotted_memory=value.current_memory + _base_mem_size 

	max_memory = float(value.max_memory)

	#Check CPU usage, regarding a 0.1 margin as eligible to scale up
	if((cpu_usage+0.1 > allotted_cpu) and (cpu_usage < max_cpu)):
		if ( obj.is_cpu_available_on_host(host, 1) ):
			#print 'Test 2'
			new_cpu_value = value.current_cpu + 1
			print "New CPU: %s" % new_cpu_value
			vm_cpu_scaling(host, vmid, value.vmip, new_cpu_value)
			manager_activity_log.write(str(datetime.datetime.now())+'::PLACEMENT MANAGER::CPU::Scaling ::'+host+' :: '+vmid+' :: Memory scaled from '+str(value.current_cpu)+' to '+str(cpu_usage)+'\n')
		else:
			print 'Test 3'
			new_host = obj.is_space_available_for_vm(cpu_usage, mem_usage , io_usage)
			if new_host is None:
    				print "Cant migrate guest"
			else:
				print 'Dest Node : '+new_host
				#Initiate vm migration
				vm_migrate_guest(host, new_host, vmid)
				manager_activity_log.write(str(datetime.datetime.now())+'::PLACEMENT MANAGER::CPU::Migration ::'+host+' :: '+vmid+' :: Domain migrated from '+str(host)+' to '+str(new_host)+' for CPU Scaling from'+str(value.current_cpu)+' to '+str(cpu_usage)+'\n')

	#if(	(cpu_usage>current_cpu) and 	(cpu_usage<max_cpu)	):  -- CPU scaling down is not implemented

	#Check Memory Usage - Memory scaling will be initiated when usage is lower than usage-scaledown_threshold or greater than usage+scaleup_threshold
	if(	(	(mem_usage > (allotted_memory + float(mem_scale_up_threshold))) or (mem_usage<(allotted_memory - float(mem_scale_down_threshold))) )and (mem_usage<max_memory)	):		
		required_extra_memory = mem_usage - allotted_memory
		if( obj.is_mem_available_on_host(host, required_extra_memory) ):
			vm_memory_scaling(host, vmid, float(mem_usage))
	    		manager_activity_log.write(str(datetime.datetime.now())+'::PLACEMENT MANAGER::MEMORY::Scaling ::'+str(host)+' :: '+str(vmid)+' :: Memory scaled from '+str(allotted_memory)+' to '+str(mem_usage)+'\n')
		else:
			new_host = obj.is_space_available_for_vm(cpu_usage, mem_usage , io_usage)
			if new_host is None:
    				print "Cant migrate Guest"
			else:
				#Initiate vm migration
				vm_migrate_guest(host, new_host, vmid)
				manager_activity_log.write(str(datetime.datetime.now())+'::PLACEMENT MANAGER::MEMORY::Migration ::'+host+' :: '+vmid+' :: Domain migrated from '+str(host)+' to '+str(new_host)+' for Memory Scaling from'+str(value.current_memory)+' to '+str(mem_usage)+'\n')



def initiateNodeLoadBalacing():
    #Initiate the module to do the node load balancing
    b=0
def initiateVMConsolidation():
    #Initiate the modeule for Vm consolidation
    c=0
def decisionManager():
    d=0
def reactOnHotSpot():
    e=0

if __name__ == "__main__":
	# stuff only to run when not called via 'import' here
	report_usage_to_placement_manager('VM_Task_16', '6.467', '8260', '0.3')
	#process_action_on_current_usage('node1', 'VM_Task_1', Guest("192.168.1.14","Task1", float(1), float(3),float(42424345353),float(424242),float(1), time.time()), '1.0', '424242', '42424345353')
