#!/usr/bin/python

import xml.dom.minidom

from xml.dom import minidom

node_dict={}

class Node:
    'Common base class for all nodes'
    nodecount = 0
    
    def __init__(self, hostname, cpu, memory, io):
        self.hostname = hostname
        self.cpu = cpu
        self.memory = memory
        self.io = io

doc = minidom.parse('nodeinfo.xml')
def getNodeText(node):
    
    nodelist = node.childNodes
    result = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            result.append(node.data)
    return ''.join(result)

nodes = doc.getElementsByTagName("node")
for node in nodes :
    hostName = getNodeText(node.getElementsByTagName("hostname")[0])
    ipaddress = getNodeText(node.getElementsByTagName("ipv4address")[0])

    capacities = node.getElementsByTagName("max_capacity")
    for capacity in capacities:
        cpu_core = getNodeText(capacity.getElementsByTagName("cpu_core")[0])
        memory = getNodeText(capacity.getElementsByTagName("memory")[0])
        io = getNodeText(capacity.getElementsByTagName("io")[0])

        node_dict[hostName]=Node(hostName, cpu_core, memory, io)

#code to print the dictionary elements
print len(node_dict)
for key, value in node_dict.iteritems() :
    print key, value.cpu, value.memory, value.io


