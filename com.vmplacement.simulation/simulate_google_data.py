#!/usr/bin/python


import os, sys, subprocess
sys.path.append('../VMPlacementAndScaling/com.vmplacement.framework')
#from . import virtds

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

def simulate_google_data():
    cmd = "pyhton /root/Desktop/VMPlacementAndScaling/com.vmplacement.manager/VM_Monitor.py &"
    os.system(cmd)
    #monitor_process = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
    for file_name in os.listdir(data_folder_path):
        if file_name.endswith(".csv"):
            #print file_name
            execute_task(file_name)
            continue
        else:
            continue

def execute_task(file_name):
    cpu_Val_cmd = 'tail -2 '+data_folder_path+'/'+file_name +' | head -1'
    cpu_val = subprocess.check_output(cpu_Val_cmd, shell=True, stderr=subprocess.PIPE)
    cpu_val=cpu_val.strip()
    mem_Val_cmd = 'tail -1 '+data_folder_path+'/'+file_name
    mem_val = subprocess.check_output(mem_Val_cmd, shell=True, stderr=subprocess.PIPE)
    mem_val = mem_val.strip()
    disk = '5242880'
    vmid=file_name[:-4]
    create_vm_cmd='python /root/Desktop/VMPlacementAndScaling/com.vmplacement.framework/virtds.py --vmid '+vmid+' --cpu '+cpu_val+' --mem '+mem_val+' --io 5242880'
    print create_vm_cmd+'\n'
    os.system(create_vm_cmd) #5 GB disk by default
                      

simulate_google_data()
