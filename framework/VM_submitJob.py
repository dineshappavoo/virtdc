#!/usr/bin/python

#The file accepts new job and create new VM with the job configuration based on the availability of hardware
#This is the part of VM placement and scaling
#This takes the VM guest configuration file from the local disk and create a new VM in current node or in a different one

import sys, getopt, subprocess, time, os
import datetime
from VM_decisionMaker import NodeFinder
from VM_Framework_Utility import getGuestIP
from VM_Info_Updater import addOrUpdateDictionaryOfVM
from Guest import Guest
from VM_RunJob import runJobOnVM
sys.path.append('/var/lib/virtdc/mail')
sys.path.append('/var/lib/virtdc/vmonere/host')
from vm_mail import send_support_mail
from vmonere_start_monitor import do_prereq_start_workload

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
# Paths and Variables
#==============================================================================

guest_image = "/home/vm_img/"
guest_config_path = "/var/lib/virtdc/framework/guestconfig.xml"
guest_config_file_storage_path = "/var/lib/virtdc/guestconfiguration/"

_master="node1"
_imageCopyCmd="scp"
_cloneCmd="virsh --connect qemu+ssh://"

_base_memory_size=2097152       # 2 GB (This includes OS memory)

#===============================================================================




def vm_submitjob(vmid,cpu,memory, max_memory, io):

    try :
	#Activity Log
	vmsubmission_log = open('/var/lib/virtdc/logs/activity_logs/vmsubmission.log', 'a+')

	obj=NodeFinder()
	#memory=float(_base_memory_size) + float(memory)
	#print "Memory "+str(memory)
    
    	#Identify is there a space for the VM
    	host = obj.is_space_available_for_vm(cpu,memory,io)


	print 'VMID "', vmid
	print 'CPU "', cpu
	print 'memory"', memory
	print 'max_memory"', max_memory
	print 'io"', io

    	if host is None:
    		print "Cant create new"
    		#print subprocess.call("date")
		#print 'VMID "', vmid
		#print 'CPU "', cpu
		#print 'memory"', memory
		#print 'max_memory"', max_memory
		#print 'io"', io
        	return False
        
	prefix_host=host
	print host
	#Code to check whether the VM can be placed
	
	if(host==_master):
		prefix_host=''
		_imageCopyCmd="cp "
		_cloneCmd="virsh create "
	else:
		_cloneCmd="virsh --connect qemu+ssh://"+host+"/system create "
		prefix_host=host+":"
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
	image_dest=prefix_host+guest_image+vmid+".img"
	cp_cmd =_imageCopyCmd+guest_image+"base_image.img "+image_dest
	copy_image = subprocess.check_output(cp_cmd, shell=True, stderr=subprocess.PIPE)
	vmsubmission_log.write(str(datetime.datetime.now()) +'::Copy Image ::'+host+' :: '+vmid+' :: Successfully copied the image\n')		

	#uuid = subprocess.check_output("uuidgen", shell=True, stderr=subprocess.PIPE)

	#config update based on the new VM requiement  	#image_path	max_memory	current_memory	current_cpu	max_cpu
	xmlstring=xmlstring.replace("vm_name", vmid);
	#xmlstring=xmlstring.replace("vm_uuid", uuid);
	xmlstring=xmlstring.replace("max_memory", str(int(max_memory)));
	xmlstring=xmlstring.replace("current_memory", str(int(memory)));
	xmlstring=xmlstring.replace("current_cpu", "1");
	xmlstring=xmlstring.replace("max_cpu", str(int(cpu)));
	xmlstring=xmlstring.replace("image_path", image_path);	

	#command to write the xml string to file
	guest_info_file=guest_config_file_storage_path + vmid+".xml"
	config_temp_file = open(guest_info_file, "w")
	config_temp_file.write(xmlstring)
	config_temp_file.close()

	#command to clone the image
	clone=_cloneCmd+guest_info_file
	clone_out = subprocess.check_output(clone, shell=True, stderr=subprocess.PIPE)
	vmsubmission_log.write(str(datetime.datetime.now()) +'::Create VM ::'+host+' :: '+vmid+' :: Successfully created the VM\n')
	
	#VM Successfully created. Update the node dictionary pickle
	host = obj.place_job (host, cpu,max_memory,io)

       	if host is None:
    		print 'Issue in updating node dictionary'
    		vmsubmission_log.write(str(datetime.datetime.now()) +'::Update Node Dictionary ::'+host+' :: '+vmid+' :: Issue in updating node dictionary\n')
		return False

	# Wait for VM to boot up
	time.sleep(60)

	#Get the IP address of Virtual Machine and update in VM_Info_Updater
	guest_ip=getGuestIP(host.strip(), vmid.strip(), "root", "Teamb@123")
	addOrUpdateDictionaryOfVM(host, vmid, Guest(guest_ip, vmid, float(1), float(cpu),float(memory),float(max_memory),float(1), str(datetime.datetime.now())  ))
	vmsubmission_log.write(str(datetime.datetime.now())+'::Update IP::'+host+' :: '+vmid+' :: Successfully updated the IP\n')
	
	# copy host_config.txt file to guest
	# this will start monitor_agent on guest
	do_prereq_start_workload(host, vmid)

	#Run Job in Guest
	runJobOnVM(host, vmid)
	vmsubmission_log.write(str(datetime.datetime.now()) +'::Run Job::'+host+' :: '+vmid+' :: Successfully ran the job\n')

	return True

    except Exception, e:
        print 'Error occured during domain creation/run job'+str(vmid)

	#exc_type, exc_obj, exc_tb = sys.exc_info()
    	#fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    	#print exc_type, fname, exc_tb.tb_lineno

        vmsubmission_log.write(str(datetime.datetime.now()) +' :: Create Guest :: '+vmid+' :: Cannot create the guest\n')
	#print "error>",e.output,'<'	
        vmsubmission_log.write(str(e) + '\n')
 	mail_subject = 'Guest creation error - '+str(vmid)
	mail_content = 'Error occured during guest creation '+vmid+' . The error as follows, \n\n'+str(e)+'\n'
	send_support_mail(mail_subject, mail_content.strip())
        return False

def main(argv):
	cpu= ''
	memory = ''
	io=''
	vmid = ''
	max_memory=4194304
	try:
		opts, args = getopt.getopt(argv,"vmid:cpu:mem:max_mem:io:",["vmid=","cpu=","mem=","max_mem=","io="])
	except getopt.GetoptError:
		print 'VM_submitjob.py --vmid <VMID> --cpu <CPU> --mem <MEMORY> --max_mem <MAX_MEMORY> --io <IO>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '--h':
			print 'VM_submitjob.py --vmid <VMID> --cpu <CPU> --mem <MEMORY> --max_mem <MAX_MEMORY> --io <IO>'
			sys.exit()
		elif opt in ("--cpu", "-cpu"):
			cpu = arg
		elif opt in ("--mem", "-mem"):
			memory = arg
		elif opt in ("--io", "-io"):
			io = arg
		elif opt in ("--vmid", "-vmid"):
			vmid = arg
		elif opt in ("--max_memory", "-max_memory"):
			max_memory = arg
	value=vm_submitjob(vmid,cpu,memory, max_memory, io)
	
if __name__ == "__main__":
	main(sys.argv[1:])
