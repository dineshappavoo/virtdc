#!/usr/bin/env python
import subprocess, sys

#API - virtdc command line init tool

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

def virtdc_init():
	#start domain termination process
	cmd = "/usr/bin/python /var/lib/virtdc/framework/VM_terminationHandler.py &"
	termination_process = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

	#initiate the vmonere socket listener
	vmonere_socket_listener_cmd = "/usr/bin/python /var/lib/virtdc/vmonere/sockets/vmonere_listener.socket.py &"
	vmonere_socket_listener = subprocess.Popen(vmonere_socket_listener_cmd, shell=True, stderr=subprocess.PIPE)

	delete_log_files_cmd = "/usr/bin/python /var/lib/virtdc/vmonere/host/vmonere_exec_log_deleter.py"
	delete_log_files_process = subprocess.Popen(delete_log_files_cmd, shell=True, stderr=subprocess.PIPE)

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   virtdc_init()

