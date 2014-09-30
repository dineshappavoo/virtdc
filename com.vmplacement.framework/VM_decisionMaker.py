#!/usr/bin/python
#from Host_machine_info_tracker import node_dict

import pickle
from Host_machine_info_tracker import Node

#Function to load the dictionary from the pickle
def loadPickleDictionary() :
	with open('node_dict.pkl', 'r') as pickle_in:
    		node_dictionary = pickle.load(pickle_in)
		return node_dictionary


#code to print the dictionary elements
print "Decision Maker"
node_dict={}
node_dict=loadPickleDictionary()

#code to print the dictionary elements
print len(node_dict)
for key, value in node_dict.iteritems() :
    print key, value.max_cpu, value.max_memory, value.max_io, value.avail_cpu, value.avail_memory, value.avail_io



#Function to place the job in the right node
def place_job(cpu, mem, io) :
	for key, value in node_dict.iteritems() :
		if (cpu <= value.avail_cpu and mem <= value.avail_memory and io <= value.avail_io) :
			value.avail_cpu=value.avail_cpu - cpu
			value.avail_memory = value.avail_memory - mem
			value.avail_io = value.avail_io - io			
			return key
	return None;


host=place_job(3,5,1)

#Code to check whether the VM can be placed
if (host is not None) :
	print host
else :
	print "Cant create new VM"

#code to print the dictionary elements again
for key, value in node_dict.iteritems() :
    print key, value.max_cpu, value.max_memory, value.max_io, value.avail_cpu, value.avail_memory, value.avail_io
