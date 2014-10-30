#!/usr/bin/python

import sys, subprocess
#API to migrate the running guest from source host to the destination host

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
#Migrating a Virtual Machine
#To migrate a virtual machine, 
#	$virsh migrate web1 qemu+ssh://desthost/system
#
#Referrence:
#       http://libvirt.org/migration.html

#-------------------------------------------------------------------------------


#Activity Log
vmmigration_log = open('../com.vmplacement.logs/activity_logs/vmmigration.log', 'a+')


def vm_migrate_guest(source_host, dest_host, vmid):

    try :

        #Initiate the module for live migration
	#migration_cmd = '''virsh migrate --live hm1 qemu+ssh://node3/system'''

	migration_cmd = "ssh -q -o StrictHostKeyChecking=no root@source_host \"virsh migrate vm_id qemu+ssh://dest_host/system\""
	migration_cmd=migration_cmd.replace("vm_id", vmid.strip());
	migration_cmd=migration_cmd.replace("source_host", source_host.strip());
	migration_cmd=migration_cmd.replace("dest_host", dest_host.strip());
	print migration_cmd
	subprocess.check_output(migration_cmd, shell=True, stderr=subprocess.PIPE)

        vmmigration_log.write('Terminate Guest ::'+source_host+' :: '+vmid+' :: Successfully migrated the guest\n')
        return True
    except Exception, e:
        print 'Cannot migrate VM '+str(vmid)+' in '+str(source_host)
        vmmigration_log.write('Migrate Guest ::'+source_host+' :: '+vmid+' :: Cannot migrate the guest\n')
        vmmigration_log.write(str(e.output) + '\n')
        return False


def vm_migrate_dependency(host, vmid):

    #change entry from host_vm_dict.pkl

    a=0


#For Testing
if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    vm_migrate_guest("node1", "node2", "VM_Task_1")


