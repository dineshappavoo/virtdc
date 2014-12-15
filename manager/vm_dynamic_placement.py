#!/usr/bin/env python
import sys, time
sys.path.append('/var/lib/virtdc/framework')
from Host_Info_Tracker import GetNodeDict
from itertools import permutations

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


node_dict = {}
PM_UTIL = {}  # PM utilization map(hexagon) (key: dimension from high util to low, value: residing PMs)

def get_max():
    node_dict = GetNodeDict()
    #for node


def start_server():
    pass

def update_pm_util(host, cpu, mem, io):
    update_dim =''

    if (cpu>=mem and mem>=io):
        update_dim = "cmi"
    elif (cpu>=io and io>=mem):
        update_dim = "cim"
    elif (mem>=cpu and cpu>=io):
        update_dim = "mci"
    elif (mem>=io and io>=cpu):
        update_dim = "mic"
    elif (io>=cpu and cpu>=mem):
        update_dim = "icm"
    elif (io>=mem and mem>=cpu):
        update_dim = "imc"


    # update PM_UTIL
    for key in PM_UTIL.iterkeys():
        if host in PM_UTIL[key]:
           if key == update_dim: 
               continue
           PM_UTIL[key].discard(host)
    else:
        PM_UTIL[update_dim].add(host)


if __name__ == "__main__":
    dimensions = ['c', 'm', 'i']
    for dim in permutations(dimensions):
        PM_UTIL.setdefault("".join(dim), set())

    start_server()
    update_pm_util("node1", 0.85, 0.75, 0.1)
update_pm_util("node2", 0.85, 0.75, 0.1)
update_pm_util("node4", 0.6, 0.75, 0.1)
update_pm_util("node3", 0.6, 0.75, 0.8)

