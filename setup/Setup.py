#!/usr/bin/python
import subprocess
import sys
import pickle
from Host_InfoTracker import GetNodeDict

#==============================================================================
# Variables
#==============================================================================

#==============================================================================

def setupAll(username, password):
	
	cmd= 'python ../setup/bridge_setup_main.py'
	uuid = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
	num = 1
	
	node_dict=GetNodeDict()
	for key, value in node_dict.iteritems() :
		innernum=1
		for innerkey, innervalue in node_dict.iteritems() :
			if innerkey != key
				cmd= 'ssh root@'+key+' \"./SSHPasswordless.sh -h '+innerkey+' -u '+username+' -p '+password+'\"'
				print cmd
				uuid = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
	
	# cmd= 'ssh '+node+' python /root/Desktop/VMPlacementAndScaling/com.vmplacement.setup/bridge_setup.py'
	# uuid = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
		

for arg in sys.argv: 
    if arg		
result = setupAll()
