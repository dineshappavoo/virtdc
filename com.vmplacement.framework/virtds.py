#!/usr/bin/python

from VM_submitJob import vm_submitjob
import sys, getopt, os

def main(argv):
	filepath=''
	cpu= ''
	memory = ''
	io=''
	vmid = ''
	fileinput=False
	#max_memory=4194304

	try:
		opts, args = getopt.getopt(argv,"t:",["f="])
		fileinput=True
	except getopt.GetoptError:
		#print 'VM_submitjob.py --vmid <VMID> --cpu <CPU> --mem <MEMORY> --io <IO>'
		try:
			opts, args = getopt.getopt(argv,"vmid:cpu:mem:io:",["vmid=","cpu=","mem=","io="])
		except getopt.GetoptError:
			print 'VM_submitjob.py --vmid <VMID> --cpu <CPU> --mem <MEMORY> --io <IO>\n'
			print 'VM_submitjob.py --f <csvfilename>\n'
			sys.exit(2)
	
	for opt, arg in opts:
		if opt == '--h':
			print 'VM_submitjob.py --vmid <VMID> --cpu <CPU> --mem <MEMORY> --io <IO>'
			sys.exit()
		if fileinput:
			if opt in ("--f", "-f"):
				csv=arg
		else:		
			if opt in ("--cpu", "-cpu"):
				cpu = arg
			elif opt in ("--mem", "-mem"):
				memory = arg
			elif opt in ("--io", "-io"):
				io = arg
			elif opt in ("--vmid", "-vmid"):
				vmid = arg			
	if fileinput:
		a=0
		# parse_cmd="python parse.py -T 26 -t "+csv
		# pass csv file as iput parser.py
		# os.system(parse_cmd)
		task_file = open('VM_Task_26.csv', 'r')
		print csv
	else :
		print vmid
		print cpu
		print memory
		print io
		vm_submitjob(vmid,cpu,memory,io)
	
if __name__ == "__main__":
	main(sys.argv[1:])
