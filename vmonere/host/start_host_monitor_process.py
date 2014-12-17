#!/usr/bin/env python
import sys, time, subprocess
sys.path.append('/var/lib/virtdc/framework')

from VM_Info_Updater import getHostVMDict
from Host_Info_Tracker import GetNodeDict
from vmonere_start_monitor import do_prereq_start_workload_host, update_host_in_config

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
host_file_path = '/var/lib/virtdc/vmonere/host/host_config.txt'

def start_host_monitor():
	master_node = 'node1'
	node_dict = GetNodeDict()
	for node in node_dict:
		if node == master_node:
			start_master_monitor_cmd = "/usr/bin/python /var/lib/virtdc/vmonere/host/vmonere_host_sender.socket &"
			print 'Test Master'
			update_host_in_config(node)
			# copy host configuration file to guest
			cpHostConfig = 'cp /var/lib/virtdc/vmonere/hostinfo/'+node+'.txt '+ host_file_path
			print cpHostConfig
			subprocess.Popen(cpHostConfig, shell=True, stderr=subprocess.PIPE)
			print start_master_monitor_cmd
			start_master_monitor = subprocess.Popen(start_master_monitor_cmd, shell=True, stderr=subprocess.PIPE)
		else:
			do_prereq_start_workload_host(node)

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   start_host_monitor()

