#!/usr/bin/python

import time
import subprocess
import pickle
import sys,os
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

def slicingIP(data, key):
        dataLen = len(data)
        for x in range(dataLen):
                #print 'data:' +data[x]+' key:'+key
                if data[x]==key:
                        lengthCut=x
                        data=data[:lengthCut]
        return data

#def slicingUsage(data, key):
#        dataLen = len(data) -1
#        for x in range(dataLen):
#                #print 'data:' +data[x]+' key:'+key
#                if data[x]==key:
#                        lengthCut=x
#                        data=data[:lengthCut]
#        return data

def getCpuUsage(vmIp):

        cmd = 'ssh -q -o StrictHostKeyChecking=no root@' +vmIp+ ' cat /proc/loadavg | awk \'{print $1}\''
        cpuUsage = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)

        return cpuUsage.strip()


def getOSMemUsage(vmIp):
        cmd='ssh -q -o StrictHostKeyChecking=no root@' +vmIp+ ' free -m | grep \'+\' | awk \'{print $3}\''
        memUsage = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
        #memUsage = slicingUsage(memUsage , '\n') #not working. future work
        #memlen = len(memUsage )
        #memUsage = memUsage[:memlen-1]

        return memUsage.strip()

def getTaskMemUsage(vmIp):
	cmd = 'ssh -q -o StrictHostKeyChecking=no root@' +vmIp+\
	" cat /proc/`cat /root/memory.pid`/status | grep VmSize | awk '{print $2}'"
	memUsage = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
	
	return memUsage if memUsage.strip() != '' else 0

def getIoUsage(vmIp):

	cmd='ssh -q -o StrictHostKeyChecking=no root@' +vmIp+ ' iostat -d -x 1 2 | grep [a-z]da | tail -1 | awk \'{print $(NF)}\''
	#cmd='ssh root@' +vmIp+ ' free -m | grep \'+\' | awk \'{print $3}\''
	ioUsage = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
	#memUsage = slicingUsage(ioUsage , '\n') #not working. future work
	#iolen = len(ioUsage )
	#ioUsage = ioUsage[:iolen - 1]

	return ioUsage.strip()


if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
	a=0



	


