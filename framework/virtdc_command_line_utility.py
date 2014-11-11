#!/usr/bin/env python
import sys, time
from Guest import Guest
from VM_Info_Updater import getHostVMDict

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

def get_host_name(vm_id):
	host_vm_dict = getHostVMDict()
	for node, vm_dict in host_vm_dict.iteritems():
        	for vmid,value in vm_dict.iteritems():
			if vm_id is vmid:
				return node
	return None

def list_host_and_domain():
	host_vm_dict = getHostVMDict()
	print '%s%s%s' %(str('Host Name').ljust(25),str('Domain Name').ljust(25),'Status')
	print '------------------------------------------------------------------'
	for node, vm_dict in host_vm_dict.iteritems():
        	for vmid,value in vm_dict.iteritems():
			print '%s%s%s' %(str(node).ljust(25),vmid.ljust(25),'running')

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   get_host_name('Test')
