#!/usr/bin/python

import time
import subprocess
import pickle
import sys,os
from timeout import timeout
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

@timeout()
def getCpuUsage(vmIp):
	
	try:
		cmd = 'ssh -q -o StrictHostKeyChecking=no root@' +vmIp+ ' cat /proc/loadavg | awk \'{print $1}\''
		cpuUsage = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
		if cpuUsage =='': return float("0.0")

	except Exception as e:
		return float("0.0")

        return cpuUsage.strip()

@timeout()
def getOSMemUsage(vmIp):
	try:
		cmd='ssh -q -o StrictHostKeyChecking=no root@' +vmIp+ ' free -m | grep \'+\' | awk \'{print $3}\''
		memUsage = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
		if memUsage =='': return float("0.0")

	except Exception as e:
		return float("0.0")

        return memUsage.strip()

@timeout()
def getTaskMemUsage(vmIp):
	try:
		cmd = 'ssh -q -o StrictHostKeyChecking=no root@' +vmIp+\
		" cat /proc/`cat /root/memory.pid`/status | grep VmSize | awk '{print $2}'"
		memUsage = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
		if memUsage =='': return float("0.0")

	except Exception as e:
		return float("0.0")
	
	return memUsage if memUsage.strip() != '' else 0

@timeout()
def getIoUsage(vmIp):
	try:
		cmd='ssh -q -o StrictHostKeyChecking=no root@' +vmIp+ ' iostat -d -x 1 2 | grep [a-z]da | tail -1 | awk \'{print $(NF)}\''
		ioUsage = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
		if ioUsage =='': return float("0.0")

	except Exception as e:
		return float("0.0")

	return ioUsage.strip()


if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
	a=0



	

