#!/usr/bin/python

import sys, subprocess
import datetime
from Guest import Guest
from VM_Info_Updater import addOrUpdateDictionaryOfVM, getHostVMDict
from Host_Info_Tracker import resume_resources_for_cpu_scaling
#API to scale the CPU in the running guest on any Host

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
#Scaling CPU in a Virtual Machine
#To scale cpu in a virtual machine, 
#          $virsh setvcpus [domain-name, domain-id or domain-uuid] [count]

#Referrence:
#        https://help.ubuntu.com/community/KVM/Virsh
#        https://www.centos.org/docs/5/html/5.2/Virtualization/chap-Virtualization-Managing_guests_with_virsh.html

#-------------------------------------------------------------------------------


#Activity Log
vmscaling_log = open('/var/lib/virtdc/logs/activity_logs/scaling.log', 'a+')

def vm_cpu_scaling(host, vmid, cpu_count):

    #try :
	print 'START'
	scaling_cmd = '''ssh -q -o StrictHostKeyChecking=no root@host_node "virsh setvcpus vm_id cpu_count"'''
	scaling_cmd = scaling_cmd.replace("vm_id", vmid.strip());
	scaling_cmd = scaling_cmd.replace("host_node", host.strip());
	scaling_cmd = scaling_cmd.replace("cpu_count", str(int(cpu_count)));
	print scaling_cmd
	cpu_scale = subprocess.check_output(scaling_cmd, shell=True, stderr=subprocess.PIPE)
	print 'Success'
	#Call to update dictionary
	update_dictionary(host, vmid, cpu_count)
	vmscaling_log.write(str(datetime.datetime.now()) +'Scale Guest ::'+host+' :: '+vmid+' :: Successful\n')
	print 'Done'
        return True
    #except Exception as e:
        #print 'Cannot scale cpu in VM '+str(vmid)+' in '+str(host)
        #vmscaling_log.write(str(datetime.datetime.now()) +'::Scale Guest ::'+host+' :: '+vmid+' :: Cannot scale the cpu in guest\n')
	#print e
        #return False

def update_dictionary(host, vmid, cpu_count):
	host_vm_dict = getHostVMDict()
    	value = host_vm_dict[host][vmid]
	old_cpu = value.current_cpu
	required_cpu = float(cpu_count) - float(old_cpu)
	guest = Guest(value.vmip,value.vmid, float(cpu_count), value.max_cpu, value.current_memory, value.max_memory,value.io, value.start_time)
	addOrUpdateDictionaryOfVM(host, vmid, guest)
	resume_resources_for_cpu_scaling(host, vmid, guest, required_cpu)

#For Testing
if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    vm_cpu_scaling("node1","VM_Task_100","2")
