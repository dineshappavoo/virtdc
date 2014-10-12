#!/usr/bin/python

#The file accepts new job and run the job on the specified node
#This is the part of VM placement and scaling
#This takes the VM guest configuration file from the local disk and create a new VM in current node or in a different one


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
host_vm_dict={}

def loadPickleDictionary() :
	try :
		with open('host_vm_dict.pkl', 'r') as pickle_in:
			dictionary = pickle.load(pickle_in)
			return dictionary
	except:
		print 'Cannot open node_dict.pkl file'
		sys.exit(1)

def runJobOnVM(hostName, vmid):
	host_vm_dict=loadPickleDictionary()
	ip=host_vm_dict[hostName][vmid]
	
