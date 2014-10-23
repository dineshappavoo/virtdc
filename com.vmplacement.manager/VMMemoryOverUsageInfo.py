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

#Node object/class to maintain the hardware information
class VMMemoryOverUsageInfo:
    'Common base class for all Memory Over Usage'
    
    def __init__(self, vmid, over_usage_flag, over_usage_occurance, total_extra_usage, start_time):
        self.vmid = vmid
        self.over_usage_flag = over_usage_flag
        self.over_usage_occurance = over_usage_occurance
        self.total_extra_usage = total_extra_usage
        self.start_time = start_time      

