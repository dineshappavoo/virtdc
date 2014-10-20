#!/usr/bin/python
'''
This script has the utility functions for the VM framework
'''
import pexpect
import sys
import pickle
from time import sleep


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

def getGuestIP(host, vmid, username, password) : 
	#vmid = "Test_node1"
	#username = "root"
	#password = "Teamb@123"
	
	# Ensure ssh to target host is passwordless
	child = pexpect.spawn('/usr/bin/ssh ' + host)
	child.expect('\~\]\#')
	child.sendline('/usr/bin/virsh console ' + vmid)
	child.sendline('\n\n')
	i = child.expect([pexpect.TIMEOUT, '\~\]\#', 'ogin: '])
	if i == 0:  # timeout
		return
	if i == 1:  # ttyS0 is logged in, do nothing
		pass
	if i == 2:  # ttyS0 is waiting at login prompt
		child.expect('ogin: ')
		child.sendline(username)
		child.expect('assword:')
		child.sendline(password)
		child.expect('\~\]\# ')

	#To get the guest IP
	child.sendline('ifconfig | grep 192.168.1. | awk \'{print $2}\'')
	child.expect('(\d+\.\d+\.\d+\.\d+)')
	ip = child.match.group()

	child.sendline('logout')
	#sleep(2)
	child.sendline('\n\n')
	print ip
	return ip

getGuestIP('Test', 'root', 'Teamb@123')

	
	

