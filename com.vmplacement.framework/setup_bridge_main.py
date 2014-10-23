import subprocess
import sys
import pickle

#/root/Desktop/VMPlacementAndScaling/com.vmplacement.setup

def loadPickleVMDictionary() :
	try :
		with open('/root/Desktop/VMPlacementAndScaling/com.vmplacement.framework/host_vm_dict.pkl', 'r') as pickle_in:
			dictionary = pickle.load(pickle_in)
			return dictionary
	except:
		print 'Cannot open host_vm_dict.pkl file'
		sys.exit(1)

def bridgeAutomate():
	for node, vm_dict in host_vm_dict.iteritems():
		cmd= 'ssh '+node+' python /root/Desktop/VMPlacementAndScaling/com.vmplacement.setup/bridge_setup.py'
		#print cmd
		uuid = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
		print 'Bridge network setup for '+node+' is completed'

host_vm_dict=loadPickleVMDictionary()
usage=bridgeAutomate()

