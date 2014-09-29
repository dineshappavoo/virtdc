#!/usr/bin/python
from Host_machine_info_tracker import node_dict

#code to print the dictionary elements
print "Decision Maker"
print len(node_dict)
for key, value in node_dict.iteritems() :
    print key, value.cpu, value.memory, value.io