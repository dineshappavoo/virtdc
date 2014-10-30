#!/usr/bin/python

import sys, time
sys.path.append('../com.vmplacement.framework')
from VM_Info_Updater import addOrUpdateDictionaryOfVM
from Guest import Guest
from VM_migrateGuest import vm_migrate_guest
from VM_cpuScaling import vm_cpu_scaling
from VM_memoryScaling import vm_memory_scaling, vm_max_memory_scaling
from VM_terminateGuest import vm_terminate_guest

#API for VM placement manager
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
#Global variables

#Memory threshold values
mem_scale_up_threshold = '10240'	# 10 MB
mem_scale_down_threshold = '102400' 	# 100 MB
time_threshold = '300' 			# 5 minutes
_base_mem_size = 1048576       		# 1 GB (This includes OS memory)

#Log activity
manager_activity_log = open('../com.vmplacement.logs/activity_logs/manager_activity.log', 'a+')

def initiateLiveMigration(vmid,sourcenode,destnode):
	a=0


#Not used
def makeMemSaclingDecision(hostName,guest,memoryUsage,time):
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

#Process current usage and take action based on SLA
def process_action_on_current_usage(host, vmid, value, cpu_usage, mem_usage, io_usage):

	max_cpu = value.max_cpu
	allotted_cpu = value.current_cpu

	#Base OS should not go below the minimum memory
	mem_usage = mem_usage + _base_mem_size 

	allotted_memory=value.current_memory + _base_mem_size 
	max_memory = value.max_memory
	#Check CPU usage
	if(	(cpu_usage>allotted_cpu) and 	(cpu_usage<max_cpu)	):
		vm_cpu_scaling(host, vmid, float(cpu_usage))
		#update vm_host_dict
		addOrUpdateDictionaryOfVM(host, vmid, Guest(value.vmip,value.vmid, float(cpu_usage), value.max_cpu,value.current_memory,value.max_memory,value.io, value.start_time))
	#if(	(cpu_usage>current_cpu) and 	(cpu_usage<max_cpu)	):  -- CPU scaling down is not implemented

	#Check Memory Usage - Memory scaling will be initiated when usage is lower than usage-scaledown_threshold or greater than usage+scaleup_threshold
	if(	(	(mem_usage > (allotted_memory + float(mem_scale_up_threshold))) or (mem_usage<(allotted_memory - float(mem_scale_down_threshold))) )and (mem_usage<max_memory)	):
		vm_memory_scaling(host, vmid, float(mem_usage))
		#update vm_host_dict
		addOrUpdateDictionaryOfVM(host, vmid, Guest(value.vmip,value.vmid, value.current_cpu, value.max_cpu, float(mem_usage),value.max_memory,value.io, value.start_time))
    		manager_activity_log.write('PLACEMENT MANAGER::MEMORY::Scaling ::'+host+' :: '+vmid+' :: Memory scaled from '+value.alotted_memory+' to '+mem_usage+'\n')



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
   process_action_on_current_usage('node1', 'VM_Task_1', Guest("192.168.1.14","Task1", float(1), float(3),float(42424345353),float(424242),float(1), time.time()), '1.0', '424242', '42424345353')
