#!/usr/bin/python
import subprocess
import sys
import pickle
sys.path.append('../framework')
from Host_Info_Tracker import GetNodeDict
import itertools

#==============================================================================
# Variables
#==============================================================================

#==============================================================================

def setupAll():
	
	cmd= 'python ../setup/bridge_setup.py'
	uuid = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
	username = 'root'
	password = 'Teamb@123'
	
	cmd= '../setup/SSHPasswordless.sh -h '+'localhost'+' -u '+username+' -p '+password
	uuid = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
	cmd= 'cp -f ../setup/SSHPasswordless.sh /root/'
	uuid = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
	
	node_dict=GetNodeDict('../framework/node_dict.pkl')
	all_address = []
	for key, value in node_dict.iteritems() :
		all_address.append(key)
	for node in all_address:
		cmd= '../setup/SSHPasswordless.sh -h '+node+' -u '+username+' -p '+password
		uuid = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
		cmd= 'scp ../setup/SSHPasswordless.sh root@'+node+':/root/'
		uuid = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
		cmd= 'scp ../setup/ifcfg* root@'+node+':/root/'
		uuid = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
		cmd= 'scp ../setup/bridge_setup.py root@'+node+':/root/'
		uuid = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
	for n in itertools.permutations(all_address, 2):
		cmd= 'ssh root@'+n[0]+' \"/root/SSHPasswordless.sh -h '+n[0]+' -u '+username+' -p '+password+'\"'
		uuid = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
		# cmd= 'ssh root@'+n[0]+' \"python /root/bridge_setup.py'+'\"'
		# uuid = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
result = setupAll()
