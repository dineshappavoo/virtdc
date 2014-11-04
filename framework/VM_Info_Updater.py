#!/usr/bin/python
import pickle
import sys, time
from Guest import Guest
from VM_Framework_Utility import getGuestIP
from Host_Info_Tracker import GetNodeDict

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

def loadPickleDictionary() :
	try :
		with open('/var/lib/virtdc/framework/node_dict.pkl', 'r') as pickle_in:
			dictionary = pickle.load(pickle_in)
			return dictionary
	except:
		print 'Cannot open node_dict.pkl file'
		sys.exit(1)

def loadPickleHostVMDictionary() :
	try :
		with open('/var/lib/virtdc/framework/host_vm_dict.pkl', 'r') as pickle_in:
			dictionary = pickle.load(pickle_in)
			return dictionary
	except:
		print 'Cannot open host_vm_dict.pkl file'
		return None
#Not used
def getHostVMDict() :
	vm_dict=loadPickleHostVMDictionary()
	if vm_dict is not None :
		return vm_dict
	else:
		return {}

def addOrUpdateDictionaryOfVM(hostName,vmid, guest) :
	#code to add the dictionary elements
	host_vm_dict=getHostVMDict()
	node_dict=GetNodeDict()

	for key, value in node_dict.iteritems() :
		if key not in host_vm_dict :
			host_vm_dict[key]={}
            		#For Testing
			#host_vm_dict[key]={"vm1":Guest("192.168.1.14","vm1", float(1), float(3),float(42424),float(424242),float(1))}
	if(guest==None):
		del host_vm_dict[hostName][vmid]
	else:
		host_vm_dict[hostName][vmid]=guest
		pickleNodeVMDictionary(host_vm_dict)
	print host_vm_dict

def pickleNodeVMDictionary(dictionary) :
	with open('/var/lib/virtdc/framework/host_vm_dict.pkl','w') as host_vm_pickle_out:
    		pickle.dump(dictionary,host_vm_pickle_out)
		#host_vm_pickle_out.close()

#======================================================================
#			Function calls 42424345353
#======================================================================
if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   addOrUpdateDictionaryOfVM('node1', 'Task1',Guest("192.168.1.14","Task1", float(1), float(3),float(42424345353),float(424242),float(1), time.time()))
   #addOrUpdateDictionaryOfVM('', '','')

