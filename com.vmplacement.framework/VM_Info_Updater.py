#!/usr/bin/python
import pickle

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

def addEmptyDictionaryOfVM() :
	#code to add the dictionary elements
	node_dict=loadPickleDictionary()
	for key, value in node_dict.iteritems() :
		if key not in host_vm_dict :
			host_vm_dict[key]={}

def pickleNodeVMDictionary(dictionary) :
	with open('host_vm_dict.pkl','w') as host_vm_pickle_out:
    		pickle.dump(dictionary,host_vm_pickle_out)
		#host_vm_pickle_out.close()

#Function calls
addEmptyDictionaryOfVM()
pickleNodeVMDictionary(host_vm_dict)
print host_vm_dict
