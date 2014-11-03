#!/usr/bin/python

import subprocess
import pickle
import sys,os
from datetime import datetime
import sys
sys.path.append('/var/virtdc/com.vmplacement.framework')
from Guest import Guest
from VM_Info_Updater import getHostVMDict
import time
from VMMemoryOverUsageInfo import VMMemoryOverUsageInfo
from VM_Monitor_Utility import getCpuUsage, getIoUsage, getTaskMemUsage
from VM_PlacementManager import process_action_on_current_usage

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
#Global Dictionary
#host_vm_dict={}
vm_mem_over_usage_dict = {}

#Memory threshold values
mem_scale_up_threshold = '10240'	# 10 MB
mem_scale_down_threshold = '102400' 	# 100 MB
time_threshold = '1' 			# 1 minutes


def monitorAndLogAndReportHotSpot():
        usageInfo=""
        file= open('/var/virtdc/com.vmplacement.logs/monitor_logs/vmusage.log', 'a+')
	host_vm_dict=getHostVMDict()
        for node, vm_dict in host_vm_dict.iteritems():
            file.write("HOST NAME : "+node+"                	TIME : "+str(datetime.now())+'\n')
	    if(vm_dict!={}):
		file.write('VM ID\t\t|\tVM IP\t\t|\tAlloted CPU\t|\tCPU usage\t|\tAllotted memory\t|\tMemory usage\t|\tAllotted IO\t|\tIO usage\n')
            for vmid,value in vm_dict.iteritems():
                vmip = value.vmip.strip()
                cpu_usage = getCpuUsage(vmip)
                mem_usage = getTaskMemUsage(vmip)
		io_usage =  getIoUsage(vmip)

		print "Current Memory "+str(value.current_memory)
		print "Task Memory Usage"+str(mem_usage)

                #usage= 'VM ID: '+vmid+'\tVM IP: '+vmip + '\t\talloted cpu: '+str(value.current_cpu)+'\tcpu usage: ' + str(cpuUsage) + '\talotted memory: '+str(value.current_memory)+'\tmemory usage: ' + str(memUsage) + '\talotted io: '+str(value.io)+'\tio usage: ' + str(ioUsage) +"\n"

                usage= vmid+'\t|\t'+vmip + '\t|\t'+str(value.current_cpu)+'\t\t|\t' + str(cpu_usage) + '\t|\t'+str(value.current_memory)+'\t|\t' + str(mem_usage) + '\t|\t'+str(value.io)+'\t|\t' + str(io_usage) +"\n"
                usageInfo+=usage

                file.write(usage+'\n')

                if (float(cpu_usage)>float(value.current_cpu) or float(mem_usage)>float(value.current_memory)):
                    #report to VM Placement manager
                    a=0

		#Process over memory usage information based on SLA
		process_mem_over_usage(vmid, float(mem_usage), float(value.current_memory))

		#Report current usage to VM Placement manager
		process_action_on_current_usage(node, vmid, value, cpu_usage, mem_usage, io_usage)

                #print usageInfo

        file.close()
        return usageInfo

def monitorVMFrequently():
    while(1):
        monitorAndLogAndReportHotSpot()
        time.sleep(30)


print "Test"



def process_mem_over_usage(vmid, mem_usage, mem_allocated):
	
	if( float(mem_usage) >(float(mem_allocated) + float(mem_scale_up_threshold))):
		#continuing over usage
		if vmid in vm_mem_over_usage_dict:
			extra_usage = float(mem_usage) - float(mem_allocated)
			over_usage_occurance = vm_mem_over_usage_dict[vmid].over_usage_occurance
			current_extra_usage = float(vm_mem_over_usage_dict[vmid].total_extra_usage) + float(extra_usage)
			start_time = vm_mem_over_usage_dict[vmid].start_time
			
			print ' Continuing usage '+str(mem_usage)+' allocated '+str(mem_allocated)

			#Updating the dictionary
			vm_mem_over_usage_dict[vmid] = VMMemoryOverUsageInfo(vmid, True, float(over_usage_occurance)+1, current_extra_usage, start_time)
		
		#Over usage for the first time		
		else:
			print 'usage '+str(mem_usage)+' allocated '+str(mem_allocated)
			extra_usage = float(mem_usage) - float(mem_allocated)
			print "Extra usage "+str(extra_usage)

			#Adding new entry to dictionary because the over usage occurs for the first time
			vm_mem_over_usage_dict[vmid] = VMMemoryOverUsageInfo(vmid, True, 1, float(extra_usage), time.time())

	elif ( float(mem_usage) < ( float(mem_allocated) + float(mem_scale_up_threshold) ) ):
		if vmid in vm_mem_over_usage_dict:
			end_time=time.time()
			start_time = vm_mem_over_usage_dict[vmid].start_time
			time_diff = end_time - start_time
			seconds = time_diff / 60
			print "Test"+str(seconds)

			if ( float(seconds) > float(time_threshold)):
        			f= open('/var/virtdc/com.vmplacement.logs/vm_logs/'+vmid+'.dat', 'a+')
				#over_usage= 'VM ID: '+vmid+'\talotted memory: '+str(mem_allocated)+'\tmemory usage: ' + str(mem_usage) + 'over usage time duration (sec) : '+str(seconds)+"\n"	
				over_usage= 'MEMORY|'+vmid+'|'+str(mem_allocated)+'|' + str(mem_usage) + '|'+str(seconds)+"\n"	
				f.write(over_usage+'\n')
				print 'Testing'
				del vm_mem_over_usage_dict[vmid]
				

		a=0



def accumulateValue():
	
	#Testing	
	currentUsage=7.0
	memAllocated = 5.0
	vmid='VM_Task1'

	memOverUsage=False
	overUsageTime=0
	last_time = time.time()
	time.sleep(10)
	now = time.time() - last_time
	time_diff=0
	minute = now % 60
	seconds = now / 60
	print 'Next time you add blood is '+str(minute)+':'+str(seconds)
        f= open('/var/virtdc/com.vmplacement.logs/vm_logs/'+vmid+'.log', 'a+')
	if(currentUsage>memAllocated):
		memOverUsage=True
		extraUsage=memAllocated-currentUsage

#======================================================================
#			Function calls
#======================================================================
if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
	usage=monitorAndLogAndReportHotSpot()
	monitorVMFrequently()
	print usage
