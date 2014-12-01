#!/usr/bin/python


import os, sys, subprocess, time, math
sys.path.append('/var/lib/virtdc/framework')
from virtdc import create_vm
from VM_terminationHandler import find_lifetime_and_terminate_vm

#==============================================================================
# Variables
#==============================================================================
#name                = "virtdc"
#version             = "0.1.0"
#long_description    = """vmplacementandscaling is a set of API's/tools written to create virtual machines for cloud users efficiently."""
#url                 = "https://github.com/dineshappavoo/VMPlacementAndScaling"
#license             = ""

#==============================================================================

data_folder_path='/var/lib/virtdc/data/vms'
_base_memory_size=2097152       # 2 GB (This includes OS memory)


def simulate_google_data():
	#start domain termination process
	cmd = "/usr/bin/python /var/lib/virtdc/framework/VM_terminationHandler.py &"
	#os.system(cmd)
	termination_process = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

	delete_log_files_cmd = "/usr/bin/python /var/lib/virtdc/vmonere/host/vmonere_exec_log_deleter.py &"
	#os.system(cmd)
	delete_log_files_process = subprocess.Popen(delete_log_files_cmd, shell=True, stderr=subprocess.PIPE)

	for file_name in os.listdir(data_folder_path):
		if file_name.endswith(".csv"):
		    #print file_name
		    vm_status = execute_task(file_name)
		    continue
		else:
		    continue

def execute_task(file_name):
    #cpu_Val_cmd = 'tail -2 '+data_folder_path+'/'+file_name +' | head -1'
    cpu_Val_cmd = 'head -1 '+data_folder_path+'/'+file_name +' | awk \'{print $2}\''
    cpu_val = subprocess.check_output(cpu_Val_cmd, shell=True, stderr=subprocess.PIPE)
    cpu_val = cpu_val.strip()
    cpu_val = math.ceil(float(cpu_val))
    print "CPU VAL  GUGGU : "+str(cpu_val)

    current_mem_cmd = 'head -1 '+data_folder_path+'/'+file_name
    current_mem_val = subprocess.check_output(current_mem_cmd, shell=True, stderr=subprocess.PIPE)
    task_spec = current_mem_val.split()
    current_mem_val = task_spec[2] #Takes the memory value first time interval
    current_mem_val = int(_base_memory_size) + int(float(current_mem_val))
    print 'Current memory value '+str(current_mem_val)

    max_mem_val_cmd = 'tail -1 '+data_folder_path+'/'+file_name
    max_mem_val = subprocess.check_output(max_mem_val_cmd, shell=True, stderr=subprocess.PIPE)
    max_mem_val = max_mem_val.strip()
    max_mem_val = int(_base_memory_size) + int(max_mem_val)

    disk = '4194304'
    vmid=file_name[:-4]

    #create_vm_cmd='python /var/lib/virtdc/framework/virtdc.py --vmid '+vmid+' --cpu '+cpu_val+' --mem '+mem_val+' --io disk'
    #print create_vm_cmd+'\n'
    #os.system(create_vm_cmd) #4 GB disk by default

    vm_status = create_vm(vmid, cpu_val, current_mem_val, max_mem_val, disk)
    if vm_status is not True:
        while(True):
            time.sleep(15)
            #vm_current_status = execute_task(file_name)
	    vm_status = create_vm(vmid, cpu_val, current_mem_val, max_mem_val, disk)
            if vm_status is True:
                break
    return vm_status


                      
if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   simulate_google_data()

