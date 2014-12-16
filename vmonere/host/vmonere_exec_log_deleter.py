#!/usr/bin/python 
import subprocess

def exec_log_deleter():
	cmd='/var/lib/virtdc/vmonere/host/vmonere_log_deleter.sh &'
	check=subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT)
	return

def kill_log_deleter():
	cmd='killall log_deleter.sh'
	check=subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT)
	return 


if __name__ == "__main__":
	# stuff only to run when not called via 'import' here
	exec_log_deleter()
