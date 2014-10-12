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
class Node:
    'Common base class for all nodes'
    nodecount = 0
    
    def __init__(self, hostname, max_cpu, max_memory, max_io, avail_cpu, avail_memory, avail_io):
        self.hostname = hostname
        self.max_cpu = max_cpu
        self.max_memory = max_memory
        self.max_io = max_io
        self.avail_cpu = avail_cpu
        self.avail_memory = avail_memory
        self.avail_io = avail_io
