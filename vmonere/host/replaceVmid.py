#!/usr/bin/python
import subprocess
import sys

def replaceVmid(vmid):
	srcPath='/var/lib/virtdc/vmonere/guest/host_config.txt'
	dstPath='/var/lib/virtdc/vmonere/dominfo/'+vmid+'.txt'
	
	value_vmid='vmid = '+vmid

	srcFile=file(srcPath)
	dstFile=open(dstPath, 'w')
	for line in srcFile.readlines():
		if line[0]=='v' and line[1]=='m' and line[2]=='i' and line[3]=='d':
			dstFile.writelines(value_vmid)
		else:
			dstFile.writelines(line)
	dstFile.writelines('\n')
	srcFile.close()
	dstFile.close()

