#!/usr/bin/python

import sys, subprocess
#API to terminate the running guest in the Host

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

#-------------------------------------------------------------------------------
#Deleting a Virtual Machine
#To delete a virtual machine, first terminate it (if running), and then undefine it
#Referrence:
#        https://help.ubuntu.com/community/KVM/Virsh
#        https://www.centos.org/docs/5/html/5.2/Virtualization/chap-Virtualization-Managing_guests_with_virsh.html

#-------------------------------------------------------------------------------


#Activity Log
vmtermination_log = open('../com.vmplacement.logs/activity_logs/vmtermination.log', 'a+')


def vm_terminate_guest(host, vmid):

    vm_destroy_cmd = 'virsh destroy '+str(vmid)
    vm_undefine_cmd = 'virsh undefine '+str(vmid)

    vm_destroy = subprocess.check_output(vm_destroy_cmd, shell=True, stderr=subprocess.PIPE)
    vm_undefine = subprocess.check_output(vm_undefine_cmd, shell=True, stderr=subprocess.PIPE)

    vmsubmission_log.write('Terminate Guest ::'+host+' :: '+vmid+' :: Successfully terminated the guest\n')


#For Testing
if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    vm_terminate_guest("node1","Test_node1")


