#!/usr/bin/python
#from Host_machine_info_tracker import node_dict

import pickle
import imp
#from Node 
from Node import Node
#newNode=
# imp.reload(Node)
from Host_Info_Tracker import pickleAddOrUpdateDictionary, GetNodeDict

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
		try :
			with open('../com.vmplacement.framework/node_dict.pkl', 'r') as pickle_in:
    				dictionary = pickle.load(pickle_in)
				return dictionary
		except:
			print 'Cannot open node_dict.pkl file'
			sys.exit(1)


    def is_space_available_for_vm(self, cpu, mem, io):
        node_dict={}
        node_dict=GetNodeDict()
        for key, value in node_dict.iteritems() :
            if ( float(cpu) <= float(value.avail_cpu) and float(	mem) <= float(value.avail_memory) and float(io) <= float(value.avail_io)) :
                return value.hostname
        return None
    
	#Function to place the job in the right node
	#@staticmethod
	def place_job(self, host, cpu, mem, io) :
		node_dict={}
		node_dict=GetNodeDict()	
		print " DECISION MAKER "
		for key, value in node_dict.iteritems() :
    			print key, value.max_cpu, value.max_memory, value.max_io, value.avail_cpu, value.avail_memory, value.avail_io
		print " DECISION MAKER END "
		for key, value in node_dict.iteritems() :
			if ( key = host ) :
				print "Test Host"+str(value.hostname)
				print value
				print "avail CPU : "+str(value.avail_cpu)
				print ''
				pickleAddOrUpdateDictionary(value.hostname, str(value.ip_address), float(value.max_cpu), float(value.max_memory), float(value.max_io), float(value.avail_cpu) - float(cpu), float(value.avail_memory) - float(mem), float(value.avail_io) -  float(io))			
				#value.avail_cpu= int(value.avail_cpu) - int(cpu)
				#value.avail_memory = int(value.avail_memory) - int(mem)
				#value.avail_io = int(value.avail_io) -  int(io)

				#Code to update the dictionary again
				#with open('node_dict.pkl','w') as node_pickle_out:
    				#	pickle.dump(node_dict,node_pickle_out)
				return value.hostname
		return None



#======================================================================
#			FOR TESTING
#======================================================================
#obj=NodeFinder()
#host = obj.place_job (1,4194304,15353)
#host=place_job(1,4194304,1)
#print host

#Code to check whether the VM can be placed
#if (host is not None) :
#	print host
#else :
#	print "Cant create new VM"

#code to print the dictionary elements again
#for key, value in node_dict.iteritems() :
#    print key, value.max_cpu, value.max_memory, value.max_io, value.avail_cpu, value.avail_memory, value.avail_io
