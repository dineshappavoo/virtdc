#!/usr/bin/python

import xml.dom.minidom
import pickle
from xml.dom import minidom

node_dict={}

#Node object/class to maintain the hardware information
class Node:
    'Common base class for all nodes'
    nodecount = 0
    
    def __init__(self, hostname, max_cpu, max_memory, max_io, avail_cpu, avail_memory, avail_io):
        self.hostname = hostname
        self.max_cpu = max_cpu
        self.max_memory = max_memory
        self.max_io = max_io
        self.avail_cpu = avail_cpu
        self.avail_memory = avail_memory
        self.avail_io = avail_io



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
	for node in nodes :
    		hostName = getNodeText(node.getElementsByTagName("hostname")[0])
    		ipaddress = getNodeText(node.getElementsByTagName("ipv4address")[0])

    		capacities = node.getElementsByTagName("max_capacity")
    		for capacity in capacities:
        		cpu_core = getNodeText(capacity.getElementsByTagName("cpu_core")[0])
        		memory = getNodeText(capacity.getElementsByTagName("memory")[0])
        		io = getNodeText(capacity.getElementsByTagName("io")[0])

        		node_dict[hostName]=Node(hostName, int(cpu_core), int(memory), int(io), int(cpu_core)-1, int(memory), int(io))

def pickleDictionary(dictionary) :
	with open('node_dict.pkl','w') as node_pickle_out:
    		pickle.dump(dictionary,node_pickle_out)
		#node_pickle_out.close()



parsenodeInfoAndMakeDict('nodeinfo.xml')
pickleDictionary(node_dict)


#code to print the dictionary elements
print len(node_dict)
for key, value in node_dict.iteritems() :
    print key, value.max_cpu, value.max_memory, value.max_io, value.avail_cpu, value.avail_memory, value.avail_io


