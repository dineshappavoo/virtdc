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

#==============================================================================
# Variables
#==============================================================================

#This is a independent file and it will be executed whenever there is a resource addition of removal based on nodeinfo.xml

# Some descriptive variables
#name                = "vmplacementandscaling"
#version             = "0.1"
#long_description    = """vmplacementandscaling is a set of API's/tools written to create virtual machines for cloud users efficiently."""
#url                 = "https://github.com/dineshappavoo/VMPlacementAndScaling"
#license             = ""

#==============================================================================

#node_dict={}

def loadPickleDictionary() :
	try :
		with open('../com.vmplacement.framework/node_dict.pkl', 'r') as pickle_in:
			dictionary = pickle.load(pickle_in)
			return dictionary
	except:
		print 'Cannot open node_dict.pkl file'
		return None


def GetNodeDict():
	dictionary=loadPickleDictionary()
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

def resume_resources_from_guest(source_host, vmid, guest):
	node_dict = GetNodeDict()
	host = node_dict[source_host]
	pickleAddOrUpdateDictionary(host.hostname, str(host.ip_address), float(host.max_cpu), float(host.max_memory), float(host.max_io), float(host.avail_cpu) + float(guest.max_cpu), float(host.avail_memory) + 		float(guest.max_memory), float(host.avail_io) +  float(guest.io))

def pickleAddOrUpdateDictionary(hostName, ip_address, cpu, mem, disk, avail_cpu, avail_mem, avail_disk) :
	node_dict=GetNodeDict()
	print "Pkl Update cpu"+str(avail_cpu)
	print "Pkl Update mem"+str(avail_mem)
	node_dict[hostName]=Node(str(hostName), str(ip_address), float(cpu), float(mem), float(disk), float(avail_cpu), float(avail_mem), float(avail_disk))
	with open('../com.vmplacement.framework/node_dict.pkl','w') as node_pickle_out:
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




