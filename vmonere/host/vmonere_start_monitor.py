#!/usr/bin/env python
import sys, time, subprocess
from framework.VM_Info_Updater import getHostVMDict

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
file_path = '/var/lib/virtdc/vmonere/guest/host_config.txt'

def do_prereq_start_workload(hostName, vmid):
	try:
		host_vm_dict=getHostVMDict()
		ip=host_vm_dict[hostName][vmid].vmip
		print "IP RUN "+str(ip)
		
		# copy host configuration file to guest
		scpHostConfig = 'scp -q -o StrictHostKeyChecking=no /var/lib/virtdc/dominfo/'+vmid+'.txt root@'+\
			ip+':'+file_path
		subprocess.Popen(scpHostConfig, shell=True, stderr=subprocess.PIPE)
		
		# copy task file to guest
		scpTask='scp -q -o StrictHostKeyChecking=no /var/lib/virtdc/data/vms/'+vmid+'.csv root@'+ip+':/root/task.dat'
		scpdata = subprocess.check_output(scpTask, shell=True, stderr=subprocess.PIPE)
		
		# initiate workload on guest
		startWork = 'ssh -q -o StrictHostKeyChecking=no root@'+ip+' nohup bash /root/setup.sh &'
		subprocess.Popen(startWork, shell=True, stderr=subprocess.PIPE)
	except subprocess.CalledProcessError as e: 
   		print "error>",e.output,'<'	
	
		#rebootCmd='ssh -q -o StrictHostKeyChecking=no root@'+ip+' reboot'
		#rebootGuest = subprocess.check_output(rebootCmd, shell=True, stderr=subprocess.PIPE)
		#guestNewIP = getGuestIP(vmid, 'root', 'Teamb@123')
		#updateGuestIP(hostName, vmid, guestNewIP)	#Add this function in VM_info_Updater.py	

		#jobPermCmd='ssh -q -o StrictHostKeyChecking=no root@'+ip+' chmod +x /root/task.dat'
		#jobPerm = subprocess.check_output(jobPermCmd, shell=True, stderr=subprocess.PIPE)	
	

def update_vmid_in_config(vmid):
	srcPath=file_path
	dstPath='/var/lib/virtdc/vmonere/dominfo/'+vmid+'.txt'
	
	value_vmid='vmid = '+vmid

	srcFile=file(srcPath)
	dstFile=open(dstPath, 'w')
	for line in srcFile.readlines():
		if line[0]=='v' and line[1]=='m' and line[2]=='i' and line[3]=='d':
			dstFile.writelines(value_vmid)
		else:
			dstFile.writelines(line)
	dstFile.writelines('\n')
	srcFile.close()
	dstFile.close()

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   do_prereq_start_workload("node1","Test_node1")

