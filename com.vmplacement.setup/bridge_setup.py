import subprocess
import sys

#/root/Desktop/VMPlacementAndScaling/com.vmplacement.setup

def backup(dest):
	#cmd='cp  /etc/sysconfig/network-scripts/ifcfg-em1 /etc/sysconfig/network-scripts/ifcfg-em1.backHaan'
	cmd='cp ' + dest + ' ' + dest+'.bak'
	backup = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
	return backup

def replace(src, dest):
	#cmd='cp  /etc/sysconfig/network-scripts/ifcfg-em1 /etc/sysconfig/network-scripts/ifcfg-em1.backHaan'

	#remove src file
	cmd='rm -f ' + src
	subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
	
	#copy tmp as a new em 1 file
	cmd='cp /root/haan/tmp '+src
	subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)

	#update dest
	cmd='rm -f ' + dest
	subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)

	cmd='cp /root/haan/tmp '+dest
	subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)

	#remove tmp file
	cmd='rm -f /root/haan/tmp'
	subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)


def getUUID(dest):
	#cmd='cat /etc/sysconfig/network-scripts/ifcfg-em1 | grep UUID'
	cmd= 'cat '+dest+'  | grep UUID'
	uuid = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
	return uuid 

def getMACADDR():
	cmd='ifconfig -a | grep ether | head -1 | awk \'{print $2}\''
	macaddr = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
	macaddrLen = len(macaddr )
	macaddr = macaddr[:macaddrLen-1]
	macaddr = 'HWADDR="' +macaddr+ '"'
	return macaddr

def updateBridge(src):
	#path
	#dest = '/etc/sysconfig/network-scripts/'+src
	#srcPath = '/root/haan/'+src #for test purpose
	
	dest = '/etc/sysconfig/network-scripts/'+src
	srcPath='/root/Desktop/VMPlacementAndScaling/com.vmplacement.setup/'+src

	#make backup
	backup(dest)

	#get UUID
	uuid = getUUID(dest)

	#get MAC
	macaddr = getMACADDR()

	#generate tmp
	srcFile=file(srcPath)
	tmpFile=open('/root/haan/tmp', 'w')
	for line in srcFile.readlines():
			
			if line[0]=='U' and line[1]=='U' and line[2]=='I' and line[3]=='D':
				tmpFile.writelines(uuid)
			elif line[0]=='H' and line[1]=='W' and line[2]=='A' and line[3]=='D' and line[4]=='D' and line[5]=='R':
				tmpFile.writelines(macaddr)
			else:
				tmpFile.writelines(line)
	
	srcFile.close()
	tmpFile.close()

	replace(srcPath, dest)
	print dest + ' is updated'
	
#/root/Desktop/VMPlacementAndScaling/com.vmplacement.setup
updateBridge('ifcfg-em1')
updateBridge('ifcfg-br0')

