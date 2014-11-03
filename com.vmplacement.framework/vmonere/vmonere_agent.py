#!/usr/bin/python

import sys, subprocess
import os.path
import time

#API to monitor the guest and report to the host

#==============================================================================
# Variables
#==============================================================================
# Some descriptive variables
#name                = "virtdc"
#version             = "0.1.0"
#long_description    = """vmplacementandscaling is a set of API's/tools written to create virtual machines for cloud users efficiently."""
#url                 = "https://github.com/dineshappavoo/VMPlacementAndScaling"
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


host_config_path = '''/var/vmonere/host_config.txt'''


def vmonere_agent():
	

def get_host_ip():
	
	while(1):
		if (os.path.exists(host_config_path)):
				print 'Host config file exists'
				break
		else :
			print 'Host config file does not exist'
			sleep(10)
		

	host_ip_cmd = '''cat host_config_file | awk '{print$2}' '''
	host_ip_cmd = host_ip_cmd.replace("host_ip_cmd",str(host_config_path).strip())

	host_ip = subprocess.check_output(host_config, shell=True, stderr=subprocess.PIPE)
	return host_ip

def report_usage_to_host():
	


	
