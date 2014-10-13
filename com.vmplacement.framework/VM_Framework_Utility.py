#!/usr/bin/python
'''
This script has the utility functions for the VM framework
'''
import pexpect
import sys
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
host_vm_dict={}

def loadPickleHostVMDictionary() :
	try :
		with open('host_vm_dict.pkl', 'r') as pickle_in:
			dictionary = pickle.load(pickle_in)
			return dictionary
	except:
		print 'Cannot open host_vm_dict.pkl file'
		sys.exit(1)

def getGuestIP(vmid, username, password) : 
	#vmid = "Test_node1"
	#username = "root"
	#password = "Teamb@123"
	
	child = pexpect.spawn('/usr/bin/virsh console ' + vmid)
	child.sendline('\n\n')
	child.expect('ogin: ')
	child.sendline(username)
	child.expect('assword:')
	child.sendline(password)
	child.expect(']# ')
	#To  get the guest IP
	child.sendline('ifconfig | grep 192.168 | awk \'{print $2}\'')
	child.expect('(\d+\.\d+\.\d+\.\d+)')
	ip = child.match.group()

	child.sendline('logout')
	#print ip
	return ip

def UpdatePickleForHostVMDict(host_vm_dict):
	with open('host_vm_dict.pkl','w') as host_vm_pickle_out:
    		pickle.dump(host_vm_dict,host_vm_pickle_out)

def GetIPAndUpdateVMDictionary(hostname, vmid):
	host_vm_dict=loadPickleHostVMDictionary()
	ip=getGuestIP(vmid, "root", "Teamb@123")
	host_vm_dict[hostname][vmid]=ip
	UpdatePickleForHostVMDict(host_vm_dict)

#Function calls for Testing
GetIPAndUpdateVMDictionary("node1", "Test_node1")
print host_vm_dict
	

	
	

