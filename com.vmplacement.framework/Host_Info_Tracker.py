#!/usr/bin/python

import xml.dom.minidom
import pickle
from Node import Node
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

node_dict={}

def loadPickleDictionary() :
	try :
		with open('node_dict.pkl', 'r') as pickle_in:
			dictionary = pickle.load(pickle_in)
			return dictionary
	except:
		print 'Cannot open node_dict.pkl file'
		return None


def GetNodeDict():
	dictionary=loadPickleDictionary()
	if dictionary is not None :
		node_dict=dictionary
	else : 
		node_dict={}

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
			
			if hostName not in node_dict :
        			node_dict[hostName]=Node(hostName, int(cpu_core), int(memory), int(io), int(cpu_core)-1, int(memory), int(io))

def pickleDictionary(dictionary) :
	with open('node_dict.pkl','w') as node_pickle_out:
    		pickle.dump(dictionary,node_pickle_out)
		#node_pickle_out.close()



#Function calls - follow the same order to call
GetNodeDict()
parsenodeInfoAndMakeDict('nodeinfo.xml')
pickleDictionary(node_dict)




#Testing
#code to print the dictionary elements
print len(node_dict)
for key, value in node_dict.iteritems() :
    print key, value.max_cpu, value.max_memory, value.max_io, value.avail_cpu, value.avail_memory, value.avail_io



