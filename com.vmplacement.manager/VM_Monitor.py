#!/usr/bin/python

import subprocess
import pickle
import sys,os
from datetime import datetime
import sys
sys.path.append('/root/Desktop/VMPlacementAndScaling/com.vmplacement.framework')
from Guest import Guest
import time
from VMMemoryOverUsageInfo import VMMemoryOverUsageInfo
from VM_Monitor_Utility import getCpuUsage, getMemUsage, getIoUsage, slicingIP

#==============================================================================
# Variables
#==============================================================================

# Some descriptive variables
# This will eventually be passed to the setup function, but we already need them
# for doing some other stuff so we have to declare them here.
#name                = "vmplacementandscaling"
#version             = "0.1"
#long_description    = """vmplacementandscaling is a set of API's/tools written to create virtual machines for cloud users efficiently."""
#url                 = "https://github.com/dineshappavoo/VMPlacementAndScaling"
#license             = ""

#==============================================================================
#Global Dictionary
#host_vm_dict={}
vm_mem_over_usage_dict = {}

#Memory threshold values
mem_scale_up_threshold = '10240'	# 10 MB
mem_scale_down_threshold = '102400' 	# 100 MB
time_threshold = '1' 			# 1 minutes


def loadPickleVMDictionary() :
    try :
        with open('../com.vmplacement.framework/host_vm_dict.pkl', 'r') as pickle_in:
            dictionary = pickle.load(pickle_in)
            return dictionary
    except:
        print 'Cannot open host_vm_dict.pkl file'
        sys.exit(1)


def monitorAndLogAndReportHotSpot():
        usageInfo=""
        file= open('../com.vmplacement.logs/monitor_logs/vmusage.log', 'a+')
	host_vm_dict=loadPickleVMDictionary()
        for node, vm_dict in host_vm_dict.iteritems():
            file.write("HOST NAME : "+node+"                TIME : "+str(datetime.now())+'\n')
            for vmId,value in vm_dict.iteritems():
                vmIp=slicingIP(value.vmip, '\n')
                cpuUsage = getCpuUsage(vmIp)
                memUsage = getMemUsage(vmIp)
		ioUsage =  getIoUsage(vmIp)
                usage= 'VM ID: '+vmId+'\tVM IP: '+vmIp + '\t\talloted cpu: '+str(value.current_cpu)+'\tcpu usage: ' + str(cpuUsage) + '\talotted memory: '+str(value.current_memory)+'\tmemory usage: ' + str(memUsage) + '\talotted io: '+str(value.io)+'\tio usage: ' + str(ioUsage) +"\n"
                usageInfo+=usage
                file.write(usage+'\n')
                if (float(cpuUsage)>float(value.current_cpu) or float(memUsage)>float(value.current_memory)):
                    #report to VM Placement manager
                    a=0


		process_mem_over_usage(vmId, float(memUsage), float(value.current_memory))
                #print usageInfo
        file.close()
        return usageInfo

def monitorVMFrequently():
    while(1):
        monitorAndLogAndReportHotSpot()
        time.sleep(20)


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
        			f= open('../com.vmplacement.logs/vm_logs/'+vmid+'.log', 'a+')
				over_usage= 'VM ID: '+vmid+'\talotted memory: '+str(mem_allocated)+'\tmemory usage: ' + str(mem_usage) + 'over usage time duration (sec) : '+str(seconds)+"\n"	
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
        f= open('../com.vmplacement.logs/vm_logs/'+vmid+'.log', 'a+')
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
