#!/usr/bin/python
import pickle
#from Host_machine_info_tracker import Node

#==============================================================================
# Variables
#==============================================================================

# Some descriptive variables
# This will eventually be passed to the setup function, but we already need them
# for doing some other stuff so we have to declare them here.
#name                = "vmplacementandscaling"
#version             = "0.1"
#long_description    = """vmplacementandscaling is a set of API's/tools written to create virtual machines for cloud users efficiently."""
#author              = "Dinesh Appavoo"
#author_email        = "dinesha.cit@gmail.com"
#url                 = "https://github.com/dineshappavoo/VMPlacementAndScaling"
#license             = ""
#==============================================================================


#Function to load the dictionary from the pickle
def loadPickleDictionary() :
	with open('node_dict.pkl', 'r') as pickle_in:
            node_dictionary = pickle.load(pickle_in)
        return node_dictionary

node_dict={}
node_dict=loadPickleDictionary()



#Function to place the job in the right node
def checkPMAvailabilityAndAppend(node,cpu, mem, io) :
    if (cpu <= node.avail_cpu and mem <= node.avail_memory and io <= node.avail_io) :
        value.avail_cpu=value.avail_cpu - cpu
		value.avail_memory = value.avail_memory - mem
		value.avail_io = value.avail_io - io
		return key
	return None;

#Function to perform the static VM placement. ref:On theory of VM Placement publication
def staticVMPlacement(vmList) :
    nodeIndex=0
    currentPM=node_dict.values()[nodeIndex++]
    vmNotPlacedCount=len(vmList)
    while (vmNotPlacedCount > 0):
        if(nodeIndex>len(node_dict)) :
            return "VM cant be placed"
        NumPotentialVMs=0;NumVMs=0;
        for vm in vmList:
            NumVMs=NumVMs+1
            if(checkPMAvailabilityAndAppend(currentPM,vm.cpu, vm.mem, vm.io) is not None) :
                NumPotentialVMs=NumPotentialVMs+1
        if (NumVMs==0) :
            Move to new T
        if (NumVMs > 0 and NumPotentialVMs == 0) :
            currentPM=node_dict.values[nodeIndex]




print currentPM.hostname
