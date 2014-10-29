#!/usr/bin/python

import sys
sys.path.append('../com.vmplacement.framework')
import VM_Info_Updater
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
memScaleUpThreshold = '10240'		# 10 MB
memScaledownThreshold = '102400' 	# 100 MB
timeThreshold = '300' 			# 5 minutes

#Log activity
manager_activity_log = open('../com.vmplacement.logs/manager_activity.log', 'a+')

def initiateLiveMigration(vmid,sourcenode,destnode):
    	
def initiateVMCPUScaleUp(vmid):

def initiateVMCPUScaleDown():
	
def makeCPUScalingDecision():

def initiateMemScaleUpOrDown(hostName, vmID, memorySize):
	try:
		scale_cmd='ssh -q -o StrictHostKeyChecking=no root@'+hostName+' virsh setmem '+vmID+' '+memorySize
        	memScale = subprocess.check_output(scaleup_cmd, shell=True, stderr=subprocess.PIPE)
	except getopt.GetoptError:
		manager_activity_log.write('Memory Scaling :: cannot be scaled up/down to '+memorySize+'for '+hostName+'-'+vmID)
	
def makeMemSaclingDecision(hostName,guest,memoryUsage,time):
	memoryAlloted=guest.current_memory
	maxMemory=''
	if(memoryUsage>memoryAlloted):
		if(memoryUsage<maxMemory):
			initiateMemScaleUpOrDown(hostName, guest.vmid, memoryUsage)
		else:
			requiredExtraMemory=float(memoryUsage)-float(maxMemory)
			if(requiredExtraMemory>memScaleUpThreshold):
				#report user through email
				#if needed do a memory scale up and charge more based on SLA
			else:
				initiateMemScaleUpOrDown(hostName, guest.vmid, memoryUsage)

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
