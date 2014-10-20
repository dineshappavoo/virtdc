#!/usr/bin/python

import subprocess
import pickle
import sys,os
from datetime import datetime
import sys
sys.path.append('/root/Desktop/VMPlacementAndScaling/com.vmplacement.framework')
from Guest import Guest
import time
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
host_vm_dict={}

def loadPickleVMDictionary() :
    try :
        with open('../com.vmplacement.framework/host_vm_dict.pkl', 'r') as pickle_in:
            dictionary = pickle.load(pickle_in)
            return dictionary
    except:
        print 'Cannot open host_vm_dict.pkl file'
        sys.exit(1)

def slicingIP(data, key):
        dataLen = len(data)
        for x in range(dataLen):
                #print 'data:' +data[x]+' key:'+key
                if data[x]==key:
                        lengthCut=x
                        data=data[:lengthCut]
        return data

def slicingUsage(data, key):
        dataLen = len(data) -1
        for x in range(dataLen):
                #print 'data:' +data[x]+' key:'+key
                if data[x]==key:
                        lengthCut=x
                        data=data[:lengthCut]
        return data

def getCpuUsage(vmIp):

        #check type of return
        cmd='ssh -q -o StrictHostKeyChecking=no root@'+vmIp+' uptime | awk \'{print $4}\''
        check=subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)

        if check == 'min,\n':
                cmd='ssh -q -o StrictHostKeyChecking=no root@'+vmIp+' uptime | awk \'{print $9}\''
        else:
                cmd='ssh -q -o StrictHostKeyChecking=no root@'+vmIp+' uptime | awk \'{print $8}\''
        cpuUsage = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
        cpuUsage = slicingUsage(cpuUsage, ',')

        return cpuUsage


def getMemUsage(vmIp):
        cmd='ssh -q -o StrictHostKeyChecking=no root@' +vmIp+ ' free -m | grep \'+\' | awk \'{print $3}\''
        memUsage = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
        #memUsage = slicingUsage(memUsage , '\n') #not working. future work
        memlen = len(memUsage )
        memUsage = memUsage[:memlen-1]

        return memUsage

def getIoUsage(vmIp):

	cmd='ssh -q -o StrictHostKeyChecking=no root@' +vmIp+ ' iostat -d -x 1 2 | grep sda | tail -1 | awk \'{print $14}\''
	#cmd='ssh root@' +vmIp+ ' free -m | grep \'+\' | awk \'{print $3}\''
	ioUsage = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
	#memUsage = slicingUsage(ioUsage , '\n') #not working. future work
	iolen = len(ioUsage )
	ioUsage = ioUsage[:iolen - 1]

	return ioUsage 

def monitorAndLogAndReportHotSpot():
        usageInfo=""
        file= open('../com.vmplacement.logs/monitor_logs/vmusage.log', 'a+')
        for node, vm_dict in host_vm_dict.iteritems():
            file.write("HOST NAME : "+node+"                TIME : "+str(datetime.now())+'\n')
            for vmId,value in vm_dict.iteritems():
                vmIp=slicingIP(value.vmip, '\n')
                cpuUsage = 0#getCpuUsage(vmIp)
                memUsage = 0#getMemUsage(vmIp)
		ioUsage =  0#getIoUsage(vmIp)
                usage= 'VM ID: '+vmId+'\tVM IP: '+vmIp + '\t\talloted cpu: '+str(value.current_cpu)+'\tcpu usage: ' + str(cpuUsage) + '\talotted memory: '+str(value.current_memory)+'\tmemory usage: ' + str(memUsage) + '\talotted io: '+str(value.io)+'\tio usage: ' + str(ioUsage) +"\n"
                usageInfo+=usage
                file.write(usage+'\n')
                if (float(cpuUsage)>float(value.current_cpu) or float(memUsage)>float(value.current_memory)):
                    #report to VM Placement manager
                    a=0
                #print usageInfo
        file.close()
        return usageInfo

def monitorVMFrequently():
    while(1):
        monitorAndLogAndReportHotSpot()
        time.sleep(20)


print "Test"
host_vm_dict=loadPickleVMDictionary()
usage=monitorAndLogAndReportHotSpot()
monitorVMFrequently()
print host_vm_dict
print usage
