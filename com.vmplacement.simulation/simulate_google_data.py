#!/usr/bin/python

import os, sys
#==============================================================================
# Variables
#==============================================================================
#name                = "vmplacementandscaling"
#version             = "0.1"
#long_description    = """vmplacementandscaling is a set of API's/tools written to create virtual machines for cloud users efficiently."""
#url                 = "https://github.com/dineshappavoo/VMPlacementAndScaling"
#license             = ""

#==============================================================================

data_folder_path='../com.vmplacement.data/vms'
for i in os.listdir(data_folder_path):
    if i.endswith(".csv") or i.endswith(".py"): 
        print i
        continue
    else:
        continue


