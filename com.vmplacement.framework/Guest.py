#!/usr/bin/python


#==============================================================================
# Variables
#==============================================================================

# Some descriptive variables
#name                = "vmplacementandscaling"
#version             = "0.1"
#long_description    = """vmplacementandscaling is a set of API's/tools written to create virtual machines for cloud users efficiently."""
#url                 = "https://github.com/dineshappavoo/VMPlacementAndScaling"
#license             = ""

#==============================================================================

#Guest object/class to maintain the VM information
class Guest:
    'Common base class for all guest'
    guestcount = 0
    
    def __init__(self,vmip, vmid, current_cpu, max_cpu, current_memory, max_memory, io, start_time):
        self.vmip = vmip
        self.vmid = vmid
        self.current_cpu = current_cpu
	self.max_cpu = max_cpu
	self.current_memory = current_memory
        self.max_memory = max_memory
        self.io = io
        self.start_time = start_time
