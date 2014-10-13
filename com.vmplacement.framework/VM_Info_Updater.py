#!/usr/bin/python
import pickle
import sys
from Guest import Guest

#==============================================================================
# Variables
#==============================================================================

# Some descriptive variables
#name                = "vmplacementandscaling"
#version             = "0.1"
#long_description    = """vmplacementandscaling is a set of API's/tools written to create virtual machines for cloud users efficiently."""
#url                 = "https://github.com/dineshappavoo/VMPlacementAndScaling"
#license             = ""

#==============================================================================

#Global variables
host_vm_dict={}


def loadPickleDictionary() :
	try :
		with open('node_dict.pkl', 'r') as pickle_in:
			dictionary = pickle.load(pickle_in)
			return dictionary
	except:
		print 'Cannot open node_dict.pkl file'
		sys.exit(1)

def loadPickleHostVMDictionary() :
	try :
		with open('host_vm_dict.pkl', 'r') as pickle_in:
			dictionary = pickle.load(pickle_in)
			return dictionary
	except:
		print 'Cannot open host_vm_dict.pkl file'
		return None

def getHostVMDict() :
	vm_dict=loadPickleHostVMDictionary()
	if vm_dict is not None :
		host_vm_dict=vm_dict

def addEmptyDictionaryOfVM() :
	#code to add the dictionary elements
	node_dict=loadPickleDictionary()
	for key, value in node_dict.iteritems() :
		if key not in host_vm_dict :
            #For Testing
			host_vm_dict[key]={"vm1":Guest("192.168.1.14","vm1", float(3),float(424242),float(1))}

def pickleNodeVMDictionary(dictionary) :
	with open('host_vm_dict.pkl','w') as host_vm_pickle_out:
    		pickle.dump(dictionary,host_vm_pickle_out)
		#host_vm_pickle_out.close()

#Function calls
getHostVMDict()
addEmptyDictionaryOfVM()
pickleNodeVMDictionary(host_vm_dict)

print host_vm_dict
