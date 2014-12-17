#!/usr/bin/env python
import sys, time, subprocess
sys.path.append('/var/lib/virtdc/framework')
from VM_Info_Updater import getHostVMDict
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
file_path = '/var/lib/virtdc/vmonere/guest/host_config.txt'
host_file_path = '/var/lib/virtdc/vmonere/host/host_config.txt'
host_sender_path = '/var/lib/virtdc/vmonere/host/'

def do_prereq_start_workload(hostName, vmid):
	try:
		host_vm_dict=getHostVMDict()
		print host_vm_dict
		ip=host_vm_dict[hostName][vmid].vmip
		print "IP RUN "+str(ip)
		
		update_vmid_in_config(vmid)
		# copy host configuration file to guest
		scpHostConfig = 'scp -q -o StrictHostKeyChecking=no /var/lib/virtdc/vmonere/dominfo/'+vmid+'.txt root@'+ip+':'+file_path
		subprocess.Popen(scpHostConfig, shell=True, stderr=subprocess.PIPE)

		start_monitor = 'ssh -n -q -o StrictHostKeyChecking=no root@'+ip+' \"/bin/nohup sh -c \'/bin/python /var/lib/virtdc/vmonere/guest/vmonere_sender_socket.py\' > /dev/null 2>&1 &' + '\"'
		print start_monitor
                subprocess.Popen(start_monitor, shell=True, stderr=subprocess.PIPE)
		
		
	except subprocess.CalledProcessError as e: 
   		print "error>",e.output,'<'	
	
		#rebootCmd='ssh -q -o StrictHostKeyChecking=no root@'+ip+' reboot'
		#rebootGuest = subprocess.check_output(rebootCmd, shell=True, stderr=subprocess.PIPE)
		#guestNewIP = getGuestIP(vmid, 'root', 'Teamb@123')
		#updateGuestIP(hostName, vmid, guestNewIP)	#Add this function in VM_info_Updater.py	

		#jobPermCmd='ssh -q -o StrictHostKeyChecking=no root@'+ip+' chmod +x /root/task.dat'
		#jobPerm = subprocess.check_output(jobPermCmd, shell=True, stderr=subprocess.PIPE)	

def do_prereq_start_workload_host(hostname):
	try:
		node_dict = GetNodeDict()
		ip = node_dict[hostname].ip_address
		#print "IP RUN "+str(ip)
		
		update_host_in_config(hostname)

		# copy host configuration file to guest
		scpHostConfig = 'scp -q -o StrictHostKeyChecking=no /var/lib/virtdc/vmonere/hostinfo/'+hostname+'.txt root@'+ip+':'+host_file_path
		subprocess.Popen(scpHostConfig, shell=True, stderr=subprocess.PIPE)
	
		scp_host_sender = 'scp -q -o StrictHostKeyChecking=no /var/lib/virtdc/vmonere/host/vmonere_host_sender.socket root@'+ip+':'+host_sender_path+'vmonere_host_sender.socket'
		print scp_host_sender
		subprocess.Popen(scp_host_sender, shell=True, stderr=subprocess.PIPE)

		scp_host_vmonere_util = 'scp -q -o StrictHostKeyChecking=no /var/lib/virtdc/vmonere/host/vmonere_utility.py root@'+ip+':'+host_sender_path+'vmonere_utility.py'
		print scp_host_vmonere_util
		subprocess.Popen(scp_host_vmonere_util, shell=True, stderr=subprocess.PIPE)

		scp_vmonere_timeout = 'scp -q -o StrictHostKeyChecking=no /var/lib/virtdc/vmonere/host/timeout.py root@'+ip+':'+host_sender_path+'timeout.py'
		print scp_vmonere_timeout
		subprocess.Popen(scp_vmonere_timeout, shell=True, stderr=subprocess.PIPE)

		start_monitor = 'ssh -n -q -o StrictHostKeyChecking=no root@'+ip+' \"/bin/nohup sh -c \'/bin/python /var/lib/virtdc/vmonere/host/vmonere_host_sender.socket\' > /dev/null 2>&1 &' + '\"'
		print start_monitor
                subprocess.Popen(start_monitor, shell=True, stderr=subprocess.PIPE)
		
		
	except subprocess.CalledProcessError as e: 
   		print "error>",e.output,'<'	
	
		#rebootCmd='ssh -q -o StrictHostKeyChecking=no root@'+ip+' reboot'
		#rebootGuest = subprocess.check_output(rebootCmd, shell=True, stderr=subprocess.PIPE)
		#guestNewIP = getGuestIP(vmid, 'root', 'Teamb@123')
		#updateGuestIP(hostName, vmid, guestNewIP)	#Add this function in VM_info_Updater.py	

		#jobPermCmd='ssh -q -o StrictHostKeyChecking=no root@'+ip+' chmod +x /root/task.dat'
		#jobPerm = subprocess.check_output(jobPermCmd, shell=True, stderr=subprocess.PIPE)	
	
def update_host_in_config(hostname):
	srcPath = '/var/lib/virtdc/vmonere/hostinfo/host_config.txt'
	dstPath='/var/lib/virtdc/vmonere/hostinfo/'+hostname+'.txt'
	
	value_hostname='host = '+hostname

	srcFile=file(srcPath)
	dstFile=open(dstPath, 'w')
	for line in srcFile.readlines():
		if line[0]=='h' and line[1]=='o' and line[2]=='s' and line[3]=='t':
			dstFile.writelines(value_hostname)
		else:
			dstFile.writelines(line)
	dstFile.writelines('\n')
	srcFile.close()
	dstFile.close()

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
   #do_prereq_start_workload("node1","VM_Task_12")
   do_prereq_start_workload_host("node2")
   #update_vmid_in_config("VM_Task_100")

