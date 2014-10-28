#!/usr/bin/python

import sys, subprocess
#API to scale the CPU in the running guest on any Host

#==============================================================================
# Variables
#==============================================================================
# Some descriptive variables
#name                = "vmplacementandscaling"
#version             = "0.1.0"
#long_description    = """vmplacementandscaling is a set of API's/tools written to create virtual machines for cloud users efficiently."""
#url                 = "https://github.com/dineshappavoo/VMPlacementAndScaling"
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
vmscaling_log = open('../com.vmplacement.logs/activity_logs/scaling.log', 'a+')

def vm_cpu_scaling(host, vmid, cpu_count):

    try :
	scaling_cmd = '''ssh -q -o StrictHostKeyChecking=no root@host_node "virsh setvcpus vm_id cpu_count"'''
	scaling_cmd = scaling_cmd.replace("vm_id", vmid.strip());
	scaling_cmd = scaling_cmd.replace("host_node", host.strip());
	scaling_cmd = scaling_cmd.replace("cpu_count", cpu_count.strip());
	cpu_scale = subprocess.check_output(scaling_cmd, shell=True, stderr=subprocess.PIPE)
	vmscaling_log.write('Scale Guest ::'+host+' :: '+vmid+' :: Successful\n')
        return True
    except:
        print 'Cannot scale cpu in VM '+str(vmid)+' in '+str(host)
        vmscaling_log.write('Scale Guest ::'+host+' :: '+vmid+' :: Cannot scale the cpu in guest\n')
        return False

#For Testing
if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    vm_cpu_scaling("node1","Test_node1","4")
