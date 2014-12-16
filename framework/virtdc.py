#!/usr/bin/env python
import argparse
import sys
from VM_submitJob import vm_submitjob
#from VM_terminateGuest import vm_terminate_guest
from virtdc_command_line_utility import get_host_name, list_host_and_domain, show_domain_info, \
    show_host_info, force_migrate, terminate_guest, monitorgraph, list_host_domain_information, \
    load_balance, consolidate, get_ip

#API - virtdc command line tool

#==============================================================================
# Variables
#==============================================================================
# Some descriptive variables
#name                = "virtdc"
#version             = "0.1.0"
#long_description    = """vmplacementandscaling is a set of API's/tools written to create virtual machines for cloud users efficiently."""
#url                 = "https://github.com/dineshappavoo/virtdc"
#license             = ""

#==============================================================================

def create_vm(vmid, cpu, memory, max_memory, io):
    print vmid
    print cpu
    print memory
    print io
    vm_placement_status = vm_submitjob(vmid, cpu, memory, max_memory, io)
    return vm_placement_status

def main(argv):
	
	parser = argparse.ArgumentParser(description="an api for data centers", version='virtdc 0.1.0')
	
	subparsers = parser.add_subparsers(help='Grouped command', dest='subparser_name')

	create_parser = subparsers.add_parser('create',help='create new domain from the base image')
	create_parser.add_argument('vmid', action = 'store', help ='get the vmid')
	create_parser.add_argument('cpu', action = 'store', help ='get the cpu')
	create_parser.add_argument('memory', action = 'store', help ='get memory in KiB')
	create_parser.add_argument('maxmemory', action = 'store', help ='get maximum memory in KiB')
	create_parser.add_argument('io', action = 'store', help ='get the io in KiB')

	terminate_parser = subparsers.add_parser('terminate',help='terminate running domain')
	terminate_parser.add_argument('vmid', action = 'store', help ='get the vmid')

	list_parser = subparsers.add_parser('list',help='list running domain')
	#list_parser.add_argument('hostname', action = 'store', help ='get the host')

	dominfo_parser = subparsers.add_parser('dominfo',help='domain information')
	dominfo_parser.add_argument('vmid', action = 'store', help ='get the domain id')

	hostinfo_parser = subparsers.add_parser('hostinfo',help='host information')
	hostinfo_parser.add_argument('hostname', action = 'store', help ='get the host')

	forcemigrate_parser = subparsers.add_parser('force-migrate',help='migrate domain from source host to dest host')
	forcemigrate_parser.add_argument('vmid', action = 'store', help ='get the domain')
	forcemigrate_parser.add_argument('sourcehost', action = 'store', help ='get the source host')
	forcemigrate_parser.add_argument('desthost', action = 'store', help ='get the dest host')

	removehost_parser = subparsers.add_parser('removehost',help='remove host')
	removehost_parser.add_argument('hostname', action = 'store', help ='get the host')

	loadbalance_parser = subparsers.add_parser('loadbalance',help='loadbalance host')
	#loadbalance_parser.add_argument('hostname', action = 'store', help ='get the host')

	consolidate_parser = subparsers.add_parser('consolidate',help='consolidate host')

	addhost_parser = subparsers.add_parser('addhost',help='add new host')
	addhost_parser.add_argument('hostname', action = 'store', help ='get the host')
	addhost_parser.add_argument('cpu', action = 'store', help ='get the cpu')
	addhost_parser.add_argument('memory', action = 'store', help ='get memory in KiB')
	addhost_parser.add_argument('io', action = 'store', help ='get the io in KiB')	

	getip_parser = subparsers.add_parser('getip',help='get domain ip')
	getip_parser.add_argument('vmid', action = 'store', help ='get the domain id')

	#mail api configuration
	setsmtpserver_parser = subparsers.add_parser('setsmtpserver',help='set smtp server')
	setsmtpserver_parser.add_argument('serverip', action = 'store', help ='get the server ip')

	setfrommailaddress_parser = subparsers.add_parser('setfrommailaddress',help='set from mailaddress')
	setfrommailaddress_parser.add_argument('mailid', action = 'store', help ='get the from mail address')

	addsupportmail_parser = subparsers.add_parser('addsupportmail',help='add support mail address')
	addsupportmail_parser.add_argument('mailid', action = 'store', help ='get the mail address')

	monitorcpu_parser = subparsers.add_parser('monitorgraph',help='monitor domain usage')
	monitorcpu_parser.add_argument('vmid', action = 'store', help ='get the domain id')

	args = parser.parse_args()

	if args.subparser_name == 'create':
		#print 'Call create vm_submit job'
		vmid =args.vmid
		cpu = args.cpu
		memory = args.memory
		max_memory = args.maxmemory
		io = args.io
		create_vm(vmid, cpu, memory, max_memory, io)
		
	elif args.subparser_name == 'terminate':
		#print 'Call vm_terminate job'
		vmid = args.vmid
		host_name = get_host_name(vmid)
		if host_name == None:
			print 'The requested domain '+str(vmid) +' cannot be terminated'
		else:
			print 'Host Name : '+str(host_name)
			vm_termination = terminate_guest(host_name, vmid)
			if vm_termination is False:
				print 'The requested domain '+str(vmid) +' cannot be terminated'
			else:
				print 'The requested domain '+str(vmid) +' terminated successfully'
		
	elif args.subparser_name == 'list':
		#print 'Call vm_list'
		list_host_domain_information()
	elif args.subparser_name == 'dominfo':
		#print 'Call vm_dominfo'
		vmid = args.vmid
		show_domain_info(vmid)
	elif args.subparser_name == 'hostinfo':
		#print 'Call vm_hostinfo'
		host_name = args.hostname
		dom_info = show_host_info(host_name)
		if dom_info == False:
			print 'Host name not found/not configured to this cluster'
	# Python argparse Namespace of '-' will be converted to '_'
	elif args.subparser_name == 'force-migrate':
		#print 'Call vm_migrate'
		#print args
		vmid = args.vmid
		source_host = args.sourcehost
		dest_host = args.desthost
		force_migrate(vmid, source_host, dest_host)
	elif args.subparser_name == 'removehost':
		print 'Call host_removehost'
	elif args.subparser_name == 'loadbalance':
		result = load_balance()
		if result is True:
			print 'load balance completes'
		else:
			print 'load balance failed!'
	elif args.subparser_name == 'consolidate':
		result = consolidate()
		if result is True:
                        print 'consolidate completes'
                else:
                        print 'consolidate failed!'
	elif args.subparser_name == 'addhost':
		print 'Call vm_addhost'
		#Add entry to nodeinfo XML and then run Host_Info_Tracker.py
		#So from next new domain creation will consider this space
		
	elif args.subparser_name == 'monitorgraph':
		#print 'Call vm_monitorgraph'
		vmid = args.vmid
		monitorgraph(vmid)
	elif args.subparser_name == 'getip':
		#print 'Call vm_monitorgraph'
		vmid = args.vmid
		ip_addr = get_ip(vmid)
		if ip_addr is None:
			print  'IP address not found'
		else:
			print ip_addr

	elif args.subparser_name == 'list':
		print 'Call vm_list'
	elif args.subparser_name == 'list':
		print 'Call vm_list'
	elif args.subparser_name == 'list':
		print 'Call vm_list'
	elif args.subparser_name == 'list':
		print 'Call vm_list'
	elif args.subparser_name == 'list':
		print 'Call vm_list'
	else:
		a=0


	#print args
	#print parser.parse_args(['terminate','Dinesh'])
	#print parser.parse_args(['create','Dinesh','1','64434','53445'])
	


if __name__ == "__main__":
	main(sys.argv[1:])
