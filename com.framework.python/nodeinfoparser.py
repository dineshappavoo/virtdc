#!/usr/bin/python

import xml.dom.minidom

from xml.dom import minidom

doc = minidom.parse('/Users/Dany/Documents/VMPlacementAndScaling/VMPlacementAndScaling/com.framework.python/nodeinfo.xml')
def getNodeText(node):
    
    nodelist = node.childNodes
    result = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            result.append(node.data)
    return ''.join(result)

nodes = doc.getElementsByTagName("node")
for node in nodes :
    hostName = node.getElementsByTagName("hostname")[0]
    ipaddress = node.getElementsByTagName("ipv4address")[0]
    print("Node Value : %s \n" % getNodeText(hostName))
    print("Node Value : %s \n" % getNodeText(ipaddress))


    capacities = node.getElementsByTagName("max_capacity")
    for capacity in capacities:
        cpu_core = capacity.getElementsByTagName("cpu_core")[0]
        memory = capacity.getElementsByTagName("memory")[0]
        io = capacity.getElementsByTagName("io")[0]
        print("CPU Core Value : %s " % getNodeText(cpu_core))
        print("Memory  Value : %s " % getNodeText(memory))
        print("IO  Value : %s " % getNodeText(io))