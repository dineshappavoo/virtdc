#!/usr/bin/python
import pickle
#from Host_machine_info_tracker import Node

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


#Function to load the dictionary from the pickle
def loadPickleDictionary() :
	with open('/var/lib/virtdc/framework/node_dict.pkl', 'r') as pickle_in:
            node_dictionary = pickle.load(pickle_in)
        return node_dictionary

node_dict={}
node_dict=loadPickleDictionary()

def abc():
    a=0

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




if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    abc()
