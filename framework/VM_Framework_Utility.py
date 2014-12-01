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
#name                = "virtdc"
#version             = "0.1.0"
#long_description    = """virtdc is a set of API's/tools written to create virtual machines for cloud users efficiently."""
#url                 = "https://github.com/dineshappavoo/virtdc"
#license             = ""

#==============================================================================

def getGuestIP(host, vmid, username, password) : 
	#vmid = "Test_node1"
	#username = "root"
	#password = "Teamb@123"
	
	# Ensure ssh to target host is passwordless
	print "Host " +str(host)
	print "VMID "+str(vmid)
	print "USER "+str(username)
	print "PASSWORD "+str(password)
	child = pexpect.spawn('/usr/bin/ssh ' + host)
	child.expect('\~\]\#')
	child.sendline('/usr/bin/virsh console ' + vmid)
	child.sendline('\n\n')
	sleep(3)
	i = child.expect([pexpect.TIMEOUT, '\~\]\#', 'ogin:'])
	
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

	sleep(3)
	#To get the guest IP
	child.sendline('ifconfig | grep 192.168.1. | awk \'{print $2}\'')
	sleep(3)
	child.expect('(\d+\.\d+\.\d+\.\d+)')
	ip = child.match.group()

	child.sendline('logout')
	#sleep(2)
	child.sendline('\n\n')
	#	print ip
	print "IP Address "+str(ip)
	return ip

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   getGuestIP('node3', 'VM_Task_20', 'root', 'Teamb@123')

	
	

