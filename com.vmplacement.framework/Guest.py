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
    
    def __init__(self,vmip, vmid, cpu, memory, io):
        self.vmip = vmip
        self.vmid = vmid
        self.cpu = cpu
        self.memory = memory
        self.io = io
