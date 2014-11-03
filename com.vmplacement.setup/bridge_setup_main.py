#!/usr/bin/python
import subprocess
import sys
import pickle

#==============================================================================
# Variables
#==============================================================================
# Some descriptive variables
#name                = "vmplacementandscaling"
#version             = "0.1.0"
#long_description    = """vmplacementandscaling is a set of API's/tools written to create virtual machines for cloud users efficiently."""
#url                 = "https://github.com/dineshappavoo/VMPlacementAndScaling"
#license             = ""

#==============================================================================

def loadPickleVMDictionary() :
	try :
		with open('/var/lib/virtdc/com.vmplacement.framework/host_vm_dict.pkl', 'r') as pickle_in:
			dictionary = pickle.load(pickle_in)
			return dictionary
	except:
		print 'Cannot open host_vm_dict.pkl file'
		sys.exit(1)

def bridgeAutomate():
	for node, vm_dict in host_vm_dict.iteritems():
		cmd= 'ssh '+node+' python /var/lib/virtdc/com.vmplacement.setup/bridge_setup.py'
		#print cmd
		uuid = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
		print 'Bridge network setup for '+node+' is completed'

host_vm_dict=loadPickleVMDictionary()
usage=bridgeAutomate()
