#!/usr/bin/python


import os, sys, subprocess
sys.path.append('/root/Desktop/VMPlacementAndScaling/com.vmplacement.framework')
from virtds import create_vm

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
_base_memory_size=1048576       # 1 GB (This includes OS memory)


def simulate_google_data():
    #cmd = "python /root/Desktop/VMPlacementAndScaling/com.vmplacement.manager/VM_Monitor.py &"
    #os.system(cmd)
    #monitor_process = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
    for file_name in os.listdir(data_folder_path):
        if file_name.endswith(".csv"):
            #print file_name
            vm_status = execute_task(file_name)
            continue
        else:
            continue

def execute_task(file_name):
    cpu_Val_cmd = 'tail -2 '+data_folder_path+'/'+file_name +' | head -1'
    cpu_val = subprocess.check_output(cpu_Val_cmd, shell=True, stderr=subprocess.PIPE)
    cpu_val = cpu_val.strip()
    mem_Val_cmd = 'tail -1 '+data_folder_path+'/'+file_name
    mem_val = subprocess.check_output(mem_Val_cmd, shell=True, stderr=subprocess.PIPE)
    mem_val = mem_val.strip()
    mem_val = int(_base_memory_size) + int(mem_val)

    disk = '4194304'
    vmid=file_name[:-4]

    #create_vm_cmd='python /root/Desktop/VMPlacementAndScaling/com.vmplacement.framework/virtds.py --vmid '+vmid+' --cpu '+cpu_val+' --mem '+mem_val+' --io disk'
    #print create_vm_cmd+'\n'
    #os.system(create_vm_cmd) #4 GB disk by default

    vm_status = create_vm(vmid, cpu_val, mem_val, disk)
    if vm_status is not True:
        while(true):
            time.sleep(15)
            vm_current_status = execute_task(file_name)
            if vm_current_status is True:
                vm_status = vm_current_status
                break
    return vm_status


                      

simulate_google_data()
