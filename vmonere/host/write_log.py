#!/usr/bin/env python

import sys, subprocess
import json, time


#==============================================================================
# Variables
#==============================================================================

# Some descriptive variables
#name                = "virtdc"
#version             = "0.1.0"
#long_description    = """virtdc is a set of API's/tools written to create virtual machines for cloud users efficiently."""
#url                 = "https://github.com/dineshappavoo/virtdc"
#license             = ""

#==============================================================================

dict = {}
def dump_json():

    now = time.time()
    dict["time"] = now

    dict["cpu"] = 51
    dict["memory"] = 52
    dict["io"] = 53
        
    with open("/Users/Dany/Downloads/my.json","w") as f:
        json.dump(dict,f)

def access_json():
    with open("/Users/Dany/Downloads/my.json") as log_file:
        log_dict = json.load(log_file)
    print log_dict

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   dump_json()
   access_json()

	
	
