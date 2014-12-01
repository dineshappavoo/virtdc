#!/usr/bin/python

import subprocess, os
import os.path
import time
import sys
from vmonere_utility import get_cpu_usage, get_os_mem_usage, get_task_mem_usage, get_io_usage

#API to monitor the guest and report to the host

#==============================================================================
# Variables
#==============================================================================
# Some descriptive variables
#name                = "virtdc"
#version             = "0.1.0"
#long_description    = """vmplacementandscaling is a set of API's/tools written to create virtual machines for cloud users efficiently."""
#url                 = "https://github.com/dineshappavoo/virtdc"
#license             = ""

#==============================================================================

#-------------------------------------------------------------------------------
#VM monitor
#vmonere agent gets the guest information and report to the host.
#	vmonere starts on guest boot up.
#         
#Referrence:
#       
#-------------------------------------------------------------------------------

#This file must be placed in the guest
host_config_path = '''/var/lib/virtdc/vmonere/guest/host_config.txt'''

def vmonere_agent():
	pass

def get_host_ip():	
	while(1):
		if (os.path.exists(host_config_path)):
				print 'Host config file exists'
				break
		else :
			print 'Host config file does not exist'
			time.sleep(10)		


	host_ip_cmd = '''/bin/cat host_config_file | /bin/grep \'host_ip\' | /bin/awk '{print$3}' '''
	host_ip_cmd = host_ip_cmd.replace("host_config_file",str(host_config_path).strip())

	host_ip = subprocess.check_output(host_ip_cmd, shell=True, stderr=subprocess.PIPE)
	print 'getting Ip'+str(host_ip)
	return host_ip

def get_vmid():
	vmid_cmd = '''/bin/cat host_config_file | /bin/grep \'vmid\' | /bin/awk '{print$3}' '''
	vmid_cmd = vmid_cmd.replace("host_config_file",str(host_config_path).strip())

	vmid = subprocess.check_output(vmid_cmd, shell=True, stderr=subprocess.PIPE)

	return vmid

def report_usage_to_host(host_ip, vmid):
	
	#base value
	cpu_usage = 0.0
	os_mem_usage = 0.0
	task_mem_usage = 0.0
	io_usage = 0.0

	cpu_usage = get_cpu_usage()
	os_mem_usage = get_os_mem_usage()
	task_mem_usage = get_task_mem_usage()
	io_usage = get_io_usage()

	usage = '\''+str(vmid.strip())+' | '+str(cpu_usage)+' | '+str(os_mem_usage)+' | '+str(task_mem_usage)+' | '+str(io_usage)+'\''
	#usage = "'cpu |sdbfsj |sdfsdhf |sdfvsdvfgdfvj'"
	#cmd = 'python /var/lib/virtdc/vmonere/host/vmonere_listener.py '+usage
	cmd = '/bin/ssh -n -q -o StrictHostKeyChecking=no root@host_ip \"/bin/nohup /bin/python /var/lib/virtdc/vmonere/host/vmonere_listener.py '+usage+' &\"'
	cmd = cmd.replace("host_ip",str(host_ip).strip())

	#cmd_res = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	os.system(cmd)

def report_usage_periodically():
	host_ip = get_host_ip()
	vmid = get_vmid()
	while(1):
		report_usage_to_host(host_ip, vmid)
		time.sleep(10)

if __name__ == "__main__":
	report_usage_periodically()
	
	


	
