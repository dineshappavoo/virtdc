#!/usr/local/bin/python


import sys
import math
import csv
import time

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

def calculate_vm_lifetime(file_name):
        ifile  = open(file_name, "rt")
        reader = csv.reader(ifile)
        total_time=0
        last=0
        #prevLast=0
        for row in reader:
                #secprevLast = prevLast
                prevLast = last
                last=int(row[0].partition(" ")[0])
                total_time = total_time + last
        total_time=total_time-last-prevLast #-secprevLast
        ifile.close()
        return total_time

def calculate_vm_endtime(vm_id, start_time):
        lifetime = calculate_vm_lifetime(data_folder_path+"/"+vm_id+".csv")
        end_time = (lifetime+ (start_time/60))*60
        sys.stdout.write("End time: %d   \r" % (end_time) )
        return end_time
    	

if __name__ == "__main__":
    calculate_vm_endtime('VM_Task_1', time.time())			
