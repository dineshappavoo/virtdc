#!/usr/bin/python

import subprocess


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


def monitor(iplist):
        f=file(iplist)
	usageInfo=""	
        for vmIp in f.readlines():
                if vmIp[0] != '\n':
                        vmIp=slicingIP(vmIp, '\n')
                        cpuUsage = getCpuUsage(vmIp)
                        memUsage = getMemUsage(vmIp)
                        usageInfo+= vmIp + '\t\t' + 'cpu: ' + cpuUsage + '\tmemory: ' + memUsage +"\n"
			#usageInfo+="\n"
			#print usageInfo
	return usageInfo

print "Test"
usage=monitor("iptest.txt")
print usage
