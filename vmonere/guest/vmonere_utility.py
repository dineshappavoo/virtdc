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
#long_description    = """vmplacementandscaling is a set of API's/tools written to create virtual machines for cloud users efficiently."""
#url                 = "https://github.com/dineshappavoo/virtdc"
#license             = ""

#==============================================================================

def slicing_ip(data, key):
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
def get_cpu_usage():
	
	try:
		cmd = " ps aux | grep cpuSim | awk \'{s+=$3} END {print s}\'"
		cpu_usage = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
		cpu_usage = float(cpu_usage.strip()) / 100
		if cpu_usage == float(0): return float("0.0")

	except Exception as e:
		return float("0.0")

        return cpu_usage

@timeout()
def get_host_cpu_usage():
	
	try:
		cmd = " ps aux | grep cpuSim | awk \'{s+=$3} END {print s}\'"
		cpu_usage = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
		cpu_usage = float(cpu_usage.strip()) / 100
		if cpu_usage == float(0): return float("0.0")

	except Exception as e:
		return float("0.0")

        return cpu_usage

@timeout()
def get_os_mem_usage():
	try:
		cmd=" free -m | grep \'+\' | awk \'{print $3}\'"
		mem_usage = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
		mem_usage = float(mem_usage.strip()) * 1024
		if mem_usage == float(0): return float("0.0")

	except Exception as e:
		return float("0.0")

        return mem_usage

@timeout()
def get_task_mem_usage():
	try:
		cmd = " cat /proc/`cat /root/memory.pid`/status | grep VmSize | awk '{print $2}'"
		mem_usage = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
		if mem_usage =='': return float("0.0")

	except Exception as e:
		return float("0.0")
	
	return mem_usage if mem_usage.strip() != '' else 0

@timeout()
def get_io_usage():
	try:
		cmd=" iostat -d -x 1 2 | grep [a-z]da | tail -1 | awk \'{print $(NF)}\'"
		io_usage = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
		if io_usage == '': return float("0.0")

	except Exception as e:
		return float("0.0")
	
	io_usage = float(io_usage.strip())
	return io_usage if io_usage < 100.0 else 100.0


if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
	a=0
	print get_cpu_usage()
	print get_io_usage()



	

