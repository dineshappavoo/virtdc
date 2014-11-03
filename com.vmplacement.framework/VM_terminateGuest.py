#!/usr/bin/python

import sys, subprocess
from Host_Info_Tracker import resume_resources_from_guest
from VM_Info_Updater import addOrUpdateDictionaryOfVM, getHostVMDict

#API to terminate the running guest in the Host

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
#Deleting a Virtual Machine
#To delete a virtual machine, first terminate it (if running), and then undefine it
#          $ virsh destroy foo_new
#          $ virsh undefine foo_new
#Referrence:
#        https://help.ubuntu.com/community/KVM/Virsh
#        https://www.centos.org/docs/5/html/5.2/Virtualization/chap-Virtualization-Managing_guests_with_virsh.html

#-------------------------------------------------------------------------------


#Activity Log
vmtermination_log = open('/var/virtdc/com.vmplacement.logs/activity_logs/vmtermination.log', 'a+')


def vm_terminate_guest(source_host, vmid):

    try :

        vm_destroy_cmd = 'ssh -q -o StrictHostKeyChecking=no root@source_host \"virsh destroy vm_id\"'
        #vm_undefine_cmd = 'ssh -q -o StrictHostKeyChecking=no root@source_host\"virsh undefine vm_id\"'
	
	vm_destroy_cmd = vm_destroy_cmd.replace("vm_id", vmid.strip());
	vm_destroy_cmd = vm_destroy_cmd.replace("source_host", source_host.strip());
	
	#vm_undefine_cmd = vm_undefine_cmd.replace("vm_id", vmid.strip());
	#vm_undefine_cmd = vm_undefine_cmd.replace("source_host", source_host.strip());

	print vm_destroy_cmd
	#print vm_undefine_cmd

        vm_destroy = subprocess.check_output(vm_destroy_cmd, shell=True, stderr=subprocess.PIPE)
        #vm_undefine = subprocess.check_output(vm_undefine_cmd, shell=True, stderr=subprocess.PIPE)

	print 'Terminate Guest ::'+source_host+' :: '+vmid+' :: Successfully terminated the guest\n'

        vmtermination_log.write('Terminate Guest ::'+source_host+' :: '+vmid+' :: Successfully terminated the guest\n')

	vm_terminate_dependency(source_host, vmid)

        return True
    except Exception, e:
        print 'Cannot remove VM '+str(vmid)+' in '+str(source_host)
        vmtermination_log.write('Terminate Guest ::'+source_host+' :: '+vmid+' :: Cannot terminate the guest\n')
        return False


def vm_terminate_dependency(source_host, vmid):

    #Remove entry from host_vm_dict.pkl
    #Remove the configuration XML
    host_vm_dict = getHostVMDict()
    guest = host_vm_dict[source_host][vmid]
    addOrUpdateDictionaryOfVM(source_host, vmid, None)
    resume_resources_from_guest(source_host, vmid, guest)


#For Testing
if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    vm_terminate_guest("node3","VM_Task_100")


