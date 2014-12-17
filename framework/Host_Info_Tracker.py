#!/usr/bin/python

import xml.dom.minidom
import pickle
from Node import Node

#import imp
#from Node 
#import Node
#newNode=
#imp.reload(Node)

from xml.dom import minidom

#This is a independent file and it will be executed whenever there is a resource addition of removal based on nodeinfo.xml

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

#node_dict={}

def loadPickleDictionary(path = None) :
	try :
		if(path is None):
			path = '/var/lib/virtdc/framework/node_dict.pkl'
		with open(path, 'r') as pickle_in:
			dictionary = pickle.load(pickle_in)
			return dictionary
	except:
		#print 'Cannot open node_dict.pkl file'
		return None


def GetNodeDict(path = None):
	dictionary=loadPickleDictionary(path)
	if dictionary is not None :
		return dictionary
	else : 
		node_dict={}
		return node_dict

def getNodeText(node):
    
    nodelist = node.childNodes
    result = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            result.append(node.data)
    return ''.join(result)

def parsenodeInfoAndMakeDict(filename) :
	doc = minidom.parse(filename)
	nodes = doc.getElementsByTagName("node")
	node_dict=GetNodeDict()
	for node in nodes :
    		hostName = getNodeText(node.getElementsByTagName("hostname")[0])
    		ipaddress = getNodeText(node.getElementsByTagName("ipv4address")[0])

    		capacities = node.getElementsByTagName("max_capacity")
    		for capacity in capacities:
        		cpu_core = getNodeText(capacity.getElementsByTagName("cpu_core")[0])
        		memory = getNodeText(capacity.getElementsByTagName("memory")[0])
        		io = getNodeText(capacity.getElementsByTagName("io")[0])
			
			if hostName not in node_dict :
				pickleAddOrUpdateDictionary(hostName, str(ipaddress), float(cpu_core), float(memory), float(io), float(cpu_core)-1, float(memory), float(io))
        			#node_dict[hostName]=Node(hostName, ipaddress, int(cpu_core), int(memory), int(io), int(cpu_core)-1, int(memory), int(io))

def find_max_cpu_mem_io_values():
	node_dict=GetNodeDict()
	max_cpu = ''
	max_memory = ''
	max_io = ''
	for node, value in node_dict.iteritems() :
		if(value.avail_cpu > max_cpu):
			max_cpu = value.avail_cpu
		if(value.avail_memory > max_memory):
			max_memory = value.avail_memory
		if(value.avail_io > max_io):
			max_io = value.avail_io
		print node, value.hostname, value.ip_address, value.max_cpu, value.max_memory, value.max_io, value.avail_cpu, value.avail_memory, value.avail_io

def resume_resources_from_guest(source_host, vmid, guest):
	node_dict = GetNodeDict()
	host = node_dict[source_host]
	pickleAddOrUpdateDictionary(host.hostname, str(host.ip_address), float(host.max_cpu), float(host.max_memory), float(host.max_io), float(host.avail_cpu) + float(guest.current_cpu), float(host.avail_memory) +float(guest.current_memory), float(host.avail_io) +  float(guest.io))


def update_resources_after_cpu_scaling(source_host, vmid, guest, required_cpu):
	node_dict = GetNodeDict()
	host = node_dict[source_host]
	pickleAddOrUpdateDictionary(host.hostname, str(host.ip_address), float(host.max_cpu), float(host.max_memory), float(host.max_io), float(host.avail_cpu) - float( required_cpu), float(host.avail_memory), float(host.avail_io))

def update_resources_after_mem_scaling(source_host, vmid, guest, required_memory):
	node_dict = GetNodeDict()
	host = node_dict[source_host]
	pickleAddOrUpdateDictionary(host.hostname, str(host.ip_address), float(host.max_cpu), float(host.max_memory), float(host.max_io), float(host.avail_cpu), float(host.avail_memory) - float(required_memory), float(host.avail_io))


def pickleAddOrUpdateDictionary(hostName, ip_address, cpu, mem, disk, avail_cpu, avail_mem, avail_disk) :
	node_dict=GetNodeDict()
	print "Pkl Update cpu"+str(avail_cpu)
	print "Pkl Update mem"+str(avail_mem)
	node_dict[hostName]=Node(str(hostName), str(ip_address), float(cpu), float(mem), float(disk), float(avail_cpu), float(avail_mem), float(avail_disk))
	with open('/var/lib/virtdc/framework/node_dict.pkl','w') as node_pickle_out:
    		pickle.dump(node_dict,node_pickle_out)
		#node_pickle_out.close()

	#Testing
	#code to print the dictionary elements
	print len(node_dict)
	for key, value in node_dict.iteritems() :
	    print key, value.hostname, value.ip_address, value.max_cpu, value.max_memory, value.max_io, value.avail_cpu, value.avail_memory, value.avail_io

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   parsenodeInfoAndMakeDict('nodeinfo.xml')

#======================================================================
#			FOR TESTING
#======================================================================
#Function calls - follow the same order to call
#GetNodeDict()




