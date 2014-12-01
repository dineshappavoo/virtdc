#!/usr/bin/python

import sys, subprocess
import datetime
from Host_Info_Tracker import resume_resources_from_guest
from VM_Info_Updater import addOrUpdateDictionaryOfVM, getHostVMDict
#API to migrate the running guest from source host to the destination host

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
#Migrating a Virtual Machine
#To migrate a virtual machine, 
#	$virsh migrate web1 qemu+ssh://desthost/system
#
#Referrence:
#       http://libvirt.org/migration.html

#-------------------------------------------------------------------------------


#Activity Log
vmmigration_log = open('/var/lib/virtdc/logs/activity_logs/vmmigration.log', 'a+')


def vm_migrate_guest(source_host, dest_host, vmid):

    try :
        #Initiate the module for live migration
	#migration_cmd = '''virsh migrate --live hm1 qemu+ssh://node3/system'''
	migration_cmd = "ssh -q -o StrictHostKeyChecking=no root@source_host \"virsh migrate vm_id qemu+ssh://dest_host/system\""
	migration_cmd=migration_cmd.replace("vm_id", vmid.strip());
	migration_cmd=migration_cmd.replace("source_host", source_host.strip());
	migration_cmd=migration_cmd.replace("dest_host", dest_host.strip());
	#print migration_cmd
	subprocess.check_output(migration_cmd, shell=True, stderr=subprocess.PIPE)

	vm_migrate_dependency(source_host,dest_host,vmid)
        vmmigration_log.write(str(datetime.datetime.now()) +'::Migrate Guest ::'+source_host+' :: '+vmid+' :: Successfully migrated the guest\n')
        return True
    except Exception, e:
        print 'Cannot migrate VM '+str(vmid)+' in '+str(source_host)
        vmmigration_log.write(str(datetime.datetime.now()) +'::Migrate Guest ::'+source_host+' :: '+vmid+' :: Cannot migrate the guest\n')
        vmmigration_log.write(str(e.output) + '\n')
        return False


def vm_migrate_dependency(source_host,dest_host,vmid):
    #Remove entry from host_vm_dict.pkl for the source_host
    #Add Entry to the dest_host in node_dict.pkl
    #Remove the configuration XML
    host_vm_dict = getHostVMDict()
    guest = host_vm_dict[source_host][vmid]
    addOrUpdateDictionaryOfVM(source_host, vmid, None)
    resume_resources_from_guest(source_host, vmid, guest)
    addOrUpdateDictionaryOfVM(dest_host, vmid, guest)



#For Testing
if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    vm_migrate_guest("node1", "node2", "VM_Task_1")


