#!/usr/bin/env python
import sys, time, subprocess, math, pickle
from Guest import Guest
from VM_Info_Updater import getHostVMDict
from Host_Info_Tracker import GetNodeDict
from VM_migrateGuest import vm_migrate_guest
from VM_terminateGuest import vm_terminate_guest
from lockfile import LockFile

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
	for node, value in node_dict.iteritems() :
		if node == host_name:
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
			return True
	return False

def force_migrate(vmid, source_host, dest_host):
	return vm_migrate_guest(source_host, dest_host,vmid)

def terminate_guest(host_name,vmid):
	return vm_terminate_guest(host_name, vmid)

def load_balance():
	node_list =     ['node1', 'node2', 'node3', 'node4']
	node_cpu_list = [   0,       0,       0,       0   ]
	host_vm_dict = getHostVMDict()
	vm_obj_list = []
	used_cpu_count = 0	

	for vm_dict in host_vm_dict.itervalues():
		for value in vm_dict.itervalues():
			used_cpu_count += value.current_cpu
			vm_obj_list.append(value)

	avg_cpu = int(math.ceil(used_cpu_count/len(node_list)))

	pickle_dict = {}
	lock = LockFile("/var/lib/virtdc/framework/host_vm_dict.pkl")
	try:
		lock.acquire(timeout=30)    # wait up to 30 seconds
	except LockTimeout:
		lock.break_lock()
		lock.acquire()
	while(len(vm_obj_list) > 0):
		max_cpu_vm = None

		# pick a vm with the largest cpu number
		for vm in vm_obj_list:
			if max_cpu_vm is None:
				max_cpu_vm = vm
			if vm.current_cpu > max_cpu_vm.current_cpu:
				max_cpu_vm = vm
		
		# migrate the max-cpu vm to first available node
		try:
			vm_migrate_guest(get_host_name(max_cpu_vm.vmid), node_list[-1], max_cpu_vm.vmid)
		except Exception:
			return False

		node_cpu_list[-1] += max_cpu_vm.current_cpu

		# node is saturated if it has reached its balance quorum
		if node_cpu_list[-1] >= avg_cpu:
			node_list.pop()
			node_cpu_list.pop()

		# re-populate the vm pickle file
		pickle_dict.setdefault(node_list[-1], {})
		pickle_dict[node_list[-1]][max_cpu_vm.vmid] = max_cpu_vm

		vm_obj_list.remove(max_cpu_vm)
	
	with open('/var/lib/virtdc/framework/host_vm_dict.pkl','w') as host_vm_pickle_out:
    		pickle.dump(pickle_dict, host_vm_pickle_out)
	lock.release()

	return True

def consolidate():
	pass

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
