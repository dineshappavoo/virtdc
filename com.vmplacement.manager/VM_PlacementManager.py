#!/usr/bin/python

import sys
sys.path.append('/Users/Dany/Documents/VMPlacementAndScaling/VMPlacementAndScaling/com.vmplacement.framework')
import VM_Info_Updater
from Guest import Guest

#==============================================================================
# Variables
#==============================================================================

# Some descriptive variables
# This will eventually be passed to the setup function, but we already need them
# for doing some other stuff so we have to declare them here.
#name                = "vmplacementandscaling"
#version             = "0.1"
#long_description    = """vmplacementandscaling is a set of API's/tools written to create virtual machines for cloud users efficiently."""
#url                 = "https://github.com/dineshappavoo/VMPlacementAndScaling"
#license             = ""

#==============================================================================

def initiateLiveMigration(vmid,sourcenode,destnode):
    	#Initiate the module for live migration
	#migration_cmd = '''virsh migrate --live hm1 qemu+ssh://node3/system'''

	migration_cmd = "ssh root@sourcenode \"virsh migrate vm_id qemu+ssh://dest_node/system\""
	migration_cmd=migration_cmd.replace("vm_id", vmid);
	migration_cmd=migration_cmd.replace("dest_node", destnode);
	migrate_vm = subprocess.check_output(migration_cmd, shell=True, stderr=subprocess.PIPE)		

def initiateVMCPUScaleUp(vmid):
	scalup_cmd='''ssh root@sourcenode \"virsh migrate vm_id qemu+ssh://dest_node/system\"'''

def initiateVMCPUScaleDown():
	
def makeCPUScalingDecision():

def initiateMemScaleUp():

def initiateMemScaleDown():

def makeMemSaclingDecision(guest):
	

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
