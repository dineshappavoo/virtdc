#!/usr/bin/python

import sys, subprocess
import datetime
from Guest import Guest
from VM_Info_Updater import addOrUpdateDictionaryOfVM, getHostVMDict
from Host_Info_Tracker import update_resources_after_mem_scaling
#API to scale the memory in the running guest on any Host

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

#-------------------------------------------------------------------------------
#Scaling memory in a Virtual Machine
#To scale memory in a virtual machine, 
#          $virsh setmem [domain-id or domain-name]  [count]
#          $virsh setmaxmem [domain-id or domain-name]  [count]
#In order to scale maxmem , the guest status must be checked.[Active/Inactive]
#Referrence:
#        https://help.ubuntu.com/community/KVM/Virsh
#        https://www.centos.org/docs/5/html/5.2/Virtualization/chap-Virtualization-Managing_guests_with_virsh.html

#-------------------------------------------------------------------------------


#Activity Log
vmscaling_log = open('/var/lib/virtdc/logs/activity_logs/scaling.log', 'a+')

def vm_memory_scaling(host, vmid, mem_size):

    try :
	scaling_cmd = '''ssh -q -o StrictHostKeyChecking=no root@host_node "virsh setmem vm_id mem_size"'''
	scaling_cmd = scaling_cmd.replace("vm_id", vmid.strip());
	scaling_cmd = scaling_cmd.replace("host_node", host.strip());
	scaling_cmd = scaling_cmd.replace("mem_size", str(int(mem_size)));
	mem_scale = subprocess.check_output(scaling_cmd, shell=True, stderr=subprocess.PIPE)
	#call to update dictionary
	update_dictionary(host, vmid, mem_size)
	vmscaling_log.write(str(datetime.datetime.now()) +'::MEMORY :: Scale Guest ::'+str(host)+' :: '+str(vmid)+' :: Successful\n')
        return True
    except:
        print 'Cannot scale memory in VM '+str(vmid)+' in '+str(host)
        vmscaling_log.write(str(datetime.datetime.now()) +'::MEMORY :: Scale Guest ::'+str(host)+' :: '+str(vmid)+' :: Cannot scale the cpu in guest\n')
        return False


def vm_max_memory_scaling(host, vmid, max_mem_size):

    try :
	scaling_cmd = '''ssh -q -o StrictHostKeyChecking=no root@host_node "virsh setmaxmem vm_id max_mem_size"'''
	scaling_cmd = scaling_cmd.replace("vm_id", vmid.strip());
	scaling_cmd = scaling_cmd.replace("host_node", host.strip());
	scaling_cmd = scaling_cmd.replace("max_mem_size", max_mem_size.strip());
	max_mem_scale = subprocess.check_output(scaling_cmd, shell=True, stderr=subprocess.PIPE)
        return True
    except:
        print 'Cannot scale memory in VM '+str(vmid)+' in '+str(host)
        vmscaling_log.write(str(datetime.datetime.now()) +'::MEMORY :: Scale Guest ::'+host+' :: '+vmid+' :: Cannot scale the max memory in guest\n')
        return False

def update_dictionary(host, vmid, mem_size):

	host_vm_dict = getHostVMDict()
    	value = host_vm_dict[host][vmid]
	old_memory = value.current_memory
	required_memory = float(mem_size) - float(old_memory)
	
	guest = Guest(value.vmip,value.vmid, value.current_cpu, value.max_cpu, float(mem_size), value.max_memory,value.io, value.start_time)

	#Update memory for guest in guest dictionary
	addOrUpdateDictionaryOfVM(host, vmid, guest)

	#Update memory for guest in host dictionary
	update_resources_after_mem_scaling(host, vmid, guest, required_memory)

#For Testing
if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    vm_memory_scaling("node1","VM_Task_11","2130000")
