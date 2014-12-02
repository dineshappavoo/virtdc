#!/usr/bin/env python
import sys, time, subprocess
from Guest import Guest
from VM_Info_Updater import getHostVMDict
from Host_Info_Tracker import GetNodeDict
from VM_migrateGuest import vm_migrate_guest
from VM_terminateGuest import vm_terminate_guest



import libvirt
import sys

sys.path.append('/var/lib/virtdc/vmonere/host')

from vmonere_monitorgraph import domain_monitor

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





def get_host_name(vm_id):
	host_vm_dict = getHostVMDict()
	for node, vm_dict in host_vm_dict.iteritems():
        	for vmid,value in vm_dict.iteritems():
			if vm_id == vmid:
				return node
	return None

def get_domain_object(vm_id):
	host_vm_dict = getHostVMDict()
	for node, vm_dict in host_vm_dict.iteritems():
        	for vmid,value in vm_dict.iteritems():
			if vm_id == vmid:
				return value
	return None

def list_host_and_domain():
	host_vm_dict = getHostVMDict()
	print '%s%s%s' %(str('Host Name').ljust(25),str('Domain Name').ljust(25),'Status')
	print '------------------------------------------------------------------'
	for node, vm_dict in host_vm_dict.iteritems():
        	for vmid,value in vm_dict.iteritems():
			print '%s%s%s' %(str(node).ljust(25),vmid.ljust(25),'running')

def list_host_domain_information():
	node_dict = GetNodeDict()
	print '----------------------------------------------------------'
	print '%s%s%s%s' %(str('Host Name').ljust(12), str(' Id').ljust(7),str('Domain Name').ljust(32),'Status')
	print '----------------------------------------------------------'
	for node, value in node_dict.iteritems() :
	    #print 'Host Name : '+str(node)
	    host = " "+str(node)+"     "
            #print '-------------------------------------------------'
            list_cmd="virsh --connect qemu+ssh://host_node/system list | tail -n +3 |  sed '/^$/d'  | sed \'s/^/ "+host+"/\'"
	    list_cmd = list_cmd.replace("host_node", node.strip());
	    #print list_cmd
	    #print list_cmd
	    running_domains = subprocess.check_output(list_cmd, shell=True, stderr=subprocess.PIPE)
	    #print running_domains
	    running_domains = "  "+str(running_domains.strip())
	    print(running_domains.decode(sys.stdout.encoding))
            list_cmd="virsh --connect qemu+ssh://host_node/system list | tail -n +3 |  sed '/^$/d'  | sed \'s/^/ "+host+"/\'"
	    #print key, value.hostname, value.ip_address, value.max_cpu, value.max_memory, value.max_io, value.avail_cpu, value.avail_memory, value.avail_io
	   


def show_domain_info(vm_id):
	host_vm_dict = getHostVMDict()
	for node, vm_dict in host_vm_dict.iteritems():
        	for vmid,value in vm_dict.iteritems():
			if vm_id == vmid:
				print '%s%s' %(str('Domain Name:').ljust(30),vmid)
				print '--------------------------------------------'
				print '%s%s' %(str('Host Name:').ljust(30),node)
				print '%s%s' %(str('Domain IP:').ljust(30),value.vmip)
				print '%s%s' %(str('Current CPU [core]:').ljust(30),value.current_cpu)
				print '%s%s' %(str('Maximum CPU [core]:').ljust(30),value.max_cpu)
				print '%s%s' %(str('Current Memory [KiB]:').ljust(30),value.current_memory)
				print '%s%s' %(str('Maximum Memory [KiB]:').ljust(30),value.max_memory)
				print '%s%s' %(str('Created Time:').ljust(30),value.start_time)
				#print '--------------------------------------------'
			#else : 
				#print 'Domain Not available'

def show_host_info(host_name):
	node_dict = GetNodeDict()
	value = node_dict[host_name]
	print '%s%s' %(str('Host Name:').ljust(30),host_name)
	print '--------------------------------------------'
	print '%s%s' %(str('Host IP:').ljust(30),value.ip_address)
	print '%s%s' %(str('Available CPU [core]:').ljust(30),value.avail_cpu)
	print '%s%s' %(str('Maximum CPU [core]:').ljust(30),value.max_cpu)
	print '%s%s' %(str('Available Memory [KiB]:').ljust(30),value.avail_memory)
	print '%s%s' %(str('Maximum Memory [KiB]:').ljust(30),value.max_memory)
	print '%s%s' %(str('Available Disk Space [KiB]:').ljust(30),value.avail_io)
	print '%s%s' %(str('Maximum Disk Space [KiB]:').ljust(30),value.max_io)
	#print '--------------------------------------------'

def force_migrate(vmid, source_host, dest_host):
	return vm_migrate_guest(source_host, dest_host,vmid)

def terminate_guest(host_name,vmid):
	return vm_terminate_guest(host_name, vmid)

def get_ip(vm_id):
	host_vm_dict = getHostVMDict()
	for node, vm_dict in host_vm_dict.iteritems():
		for vmid,value in vm_dict.iteritems():
			if vm_id == vmid:
				return value.vmip
	return None

def monitorgraph(vmid):
	domain_monitor(vmid)
	

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   get_host_name('Test')
