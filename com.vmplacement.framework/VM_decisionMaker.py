#!/usr/bin/python
#from Host_machine_info_tracker import node_dict

import pickle
#from Host_machine_info_tracker import Node

#==============================================================================
# Variables
#==============================================================================

# Some descriptive variables
# This will eventually be passed to the setup function, but we already need them
# for doing some other stuff so we have to declare them here.
#name                = "vmplacementandscaling"
#version             = "0.1"
#long_description    = """vmplacementandscaling is a set of API's/tools written to create virtual machines for cloud users efficiently."""
#url                 = "https://github.com/dineshappavoo/VMPlacementAndScaling"
#license             = ""

#==============================================================================
class NodeFinder:
	#Function to load the dictionary from the pickle
	#@staticmethod
	def loadPickleDictionary(self) :
		with open('node_dict.pkl', 'r') as pickle_in:
    			dictionary = pickle.load(pickle_in)
			return dictionary


	#Function to place the job in the right node
	#@staticmethod
	def place_job(self, cpu, mem, io) :
		node_dict={}
		node_dict=self.loadPickleDictionary()	
		for key, value in node_dict.iteritems() :
			if ( int(cpu) <= int(value.avail_cpu) and int(mem) <= int(value.avail_memory) and int(io) <= int(value.avail_io)) :
				print value.hostname				
				value.avail_cpu= int(value.avail_cpu) - int(cpu)
				value.avail_memory = int(value.avail_memory) - int(mem)
				value.avail_io = int(value.avail_io) -  int(io)

				#Code to update the dictionary again
				with open('node_dict.pkl','w') as node_pickle_out:
    					pickle.dump(node_dict,node_pickle_out)
				return value.hostname
		return None

#host=place_job(1,4194304,1)

#Code to check whether the VM can be placed
#if (host is not None) :
#	print host
#else :
#	print "Cant create new VM"

#code to print the dictionary elements again
#for key, value in node_dict.iteritems() :
#    print key, value.max_cpu, value.max_memory, value.max_io, value.avail_cpu, value.avail_memory, value.avail_io
