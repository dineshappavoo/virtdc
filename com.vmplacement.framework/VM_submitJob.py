#!/usr/bin/python

#The file accepts new job and create new VM with the job configuration based on the availability of hardware
#This is the part of VM placement and scaling
#This takes the VM guest configuration file from the local disk and create a new VM in current node or in a different one

import sys, getopt, subprocess
from VM_decisionMaker import NodeFinder
#from Host_machine_info_tracker import Node


#==============================================================================
# Variables
#==============================================================================

# Some descriptive variables
# This will eventually be passed to the setup function, but we already need them
# for doing some other stuff so we have to declare them here.
#name                = "vmplacementandscaling"
#version             = "0.1"
#long_description    = """vmplacementandscaling is a set of API's/tools written to create virtual machines for cloud users efficiently."""
#url                 = "https://github.com/dineshappavoo/VMPlacementAndScaling"
#license             = ""

#==============================================================================
# Paths and Variables
#==============================================================================

guest_image = "/var/lib/libvirt/images/"
guest_config_path = "/root/Desktop/PYTHON/guestconfig.xml"

_master="node1"
_imageCopyCmd="scp"
_cloneCmd="virsh --connect qemu+ssh://"

#===============================================================================


def main(argv):
	cpu= ''
	memory = ''
	io=''
	vmid = ''
	time = ''
	max_memory=4194304
	try:
		opts, args = getopt.getopt(argv,"vmid:cpu:mem:io:time:",["vmid=","cpu=","mem=","io=","time="])
	except getopt.GetoptError:
		print 'VM_submitjob.py --vmid <VMID> --cpu <CPU> --mem <MEMORY> --io <IO> --time <TIME>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '--h':
			print 'VM_submitjob.py --vmid <VMID> --cpu <CPU> --mem <MEMORY> --io <IO> --time <TIME>'
			sys.exit()
		elif opt in ("--cpu", "-cpu"):
			cpu = arg
		elif opt in ("--mem", "-mem"):
			memory = arg
		elif opt in ("--io", "-io"):
			io = arg
		elif opt in ("--vmid", "-vmid"):
			vmid = arg
		elif opt in ("--time", "-time"):
			time = arg
	obj=NodeFinder()
	host = obj.place_job (cpu,memory,io)
	print host
	
	


	#Code to check whether the VM can be placed
	if (host is not None) :
		if(host==_master):
			host=''
			_imageCopyCmd="cp "
			_cloneCmd="virsh create "
		else:
			_cloneCmd="virsh --connect qemu+ssh://"+host+"/system create "
			host=host+":"
			_imageCopyCmd="scp "

		#print "The node is %s",host
		#To get the guest os configuration xml for the first time	
		#cmd = "virsh dumpxml Test_clone > /root/Desktop/PYTHON/guestconfig.xml"
		#p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	
		#command to get the xml into python string for further updates. guestconfig.xml needs to be copied(physically present) int the same folder of this script
		nodeInfo="cat "+guest_config_path
		xmlstring = subprocess.check_output(nodeInfo, shell=True, stderr=subprocess.PIPE)
	
		#command to copy the iso image to the destination. Every VM will have an individual iso image. (I think this copy can be cleared later on). Make the nodes passwordless
		image_path=guest_image+vmid+".img"
		image_dest=host+guest_image+vmid+".img"
		cp_cmd =_imageCopyCmd+guest_image+"Test.img "+image_dest
		copy_image = subprocess.check_output(cp_cmd, shell=True, stderr=subprocess.PIPE)		
	
		uuid = subprocess.check_output("uuidgen", shell=True, stderr=subprocess.PIPE)
	
		#config update based on the new VM requiement  	#image_path	max_memory	current_memory	current_cpu	max_cpu
		xmlstring=xmlstring.replace("vm_name", vmid);
		xmlstring=xmlstring.replace("vm_uuid", uuid);
		xmlstring=xmlstring.replace("max_memory", memory);
		xmlstring=xmlstring.replace("current_memory", memory);
		xmlstring=xmlstring.replace("current_cpu", "1");
		xmlstring=xmlstring.replace("max_cpu", cpu);
		xmlstring=xmlstring.replace("image_path", image_path);	
	
		#command to write the xml string to file
		guest_info_file=vmid+".xml"
		config_temp_file = open(guest_info_file, "w")
		config_temp_file.write(xmlstring)
		config_temp_file.close()
	
		#command to clone the image
		clone=_cloneCmd+guest_info_file
		clone_out = subprocess.check_output(clone, shell=True, stderr=subprocess.PIPE)

	else :
		print "Cant create new"

	print subprocess.call("date")
	print 'VMID "', vmid
	print 'CPU "', cpu
	print 'memory"', memory
	print 'io"', io
	print 'time"', time

if __name__ == "__main__":
	main(sys.argv[1:])
