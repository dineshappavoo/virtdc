#!/usr/bin/python

import subprocess
import pickle
import sys
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

def loadPickleDictionary() :
    try :
        with open('~/framework/host_vm_dict.pkl', 'r') as pickle_in:
            dictionary = pickle.load(pickle_in)
            return dictionary
    except:
        print 'Cannot open node_dict.pkl file'
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
        cmd='ssh root@'+vmIp+' uptime | awk \'{print $4}\''
        check=subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)

        if check == 'min,\n':
                cmd='ssh root@'+vmIp+' uptime | awk \'{print $9}\''
        else:
                cmd='ssh root@'+vmIp+' uptime | awk \'{print $8}\''
        cpuUsage = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
        cpuUsage = slicingUsage(cpuUsage, ',')

        return cpuUsage


def getMemUsage(vmIp):
        cmd='ssh root@' +vmIp+ ' free -m | grep \'+\' | awk \'{print $3}\''
        memUsage = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
        #memUsage = slicingUsage(memUsage , '\n') #not working. future work
        memlen = len(memUsage )
        memUsage = memUsage[:memlen-1]

        return memUsage


def monitorLogAndReportHotSpot():
        #f=file(iplist)
        usageInfo=""
        file= open('vmusage.log', 'w+')
        for node, vm_dict in host_vm_dict.iteritems():
            for vmId,value in vm_dict:
                vmIp=slicingIP(value.vmip, '\n')
                cpuUsage = getCpuUsage(vmIp)
                memUsage = getMemUsage(vmIp)
                usage= vmId+'\t\t'+vmIp + '\t\t' + 'cpu: ' + cpuUsage + '\tmemory: ' + memUsage +"\n"
                usageInfo+=usage
                file.write(usage)
                if (float(cpuUsage)>float(value.cpu) or float(memUsage)>float(value.memory)):
                    #report to VM Placement manager
                    a=0
                #print usageInfo
        file.close()
        return usageInfo

print "Test"
usage=monitorLogAndReportHotSpot()
print usage
