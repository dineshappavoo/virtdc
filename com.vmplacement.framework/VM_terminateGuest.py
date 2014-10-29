#!/usr/bin/python

import sys, subprocess
#API to terminate the running guest in the Host

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
#Deleting a Virtual Machine
#To delete a virtual machine, first terminate it (if running), and then undefine it
#          $ virsh destroy foo_new
#          $ virsh undefine foo_new
#Referrence:
#        https://help.ubuntu.com/community/KVM/Virsh
#        https://www.centos.org/docs/5/html/5.2/Virtualization/chap-Virtualization-Managing_guests_with_virsh.html

#-------------------------------------------------------------------------------


#Activity Log
vmtermination_log = open('../com.vmplacement.logs/activity_logs/vmtermination.log', 'a+')


def vm_terminate_guest(host, vmid):

    try :

        vm_destroy_cmd = 'ssh -q -o StrictHostKeyChecking=no root@'+host+'virsh destroy '+str(vmid)
        vm_undefine_cmd = 'ssh -q -o StrictHostKeyChecking=no root@'+host+'virsh undefine '+str(vmid)

        vm_destroy = subprocess.check_output(vm_destroy_cmd, shell=True, stderr=subprocess.PIPE)
        vm_undefine = subprocess.check_output(vm_undefine_cmd, shell=True, stderr=subprocess.PIPE)

        vmtermination_log.write('Terminate Guest ::'+host+' :: '+vmid+' :: Successfully terminated the guest\n')
        return True
    except:
        print 'Cannot remove VM '+str(vmid)+' in '+str(host)
        vmtermination_log.write('Terminate Guest ::'+host+' :: '+vmid+' :: Cannot terminate the guest\n')
        return False


def vm_terminate_dependency(host, vmid):

    #Remove entry from host_vm_dict.pkl
    #Remove the configuration XML
    a=0


#For Testing
if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    vm_terminate_guest("node1","Test_node1")


