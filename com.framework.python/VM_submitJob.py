#!/usr/bin/python

import sys, getopt, subprocess

def main(argv):
    cpu= ''
    memory = ''
    vmid = ''
    time = ''
    try:
        opts, args = getopt.getopt(argv,"vmid:cpu:mem:time:",["vmid=","cpu=","mem=","time="])
    except getopt.GetoptError:
        print 'VM_submitjob.py --vmid <VMID> --cpu <CPU> --mem <MEMORY> --time <TIME>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '--h':
            print 'VM_submitjob.py --vmid <VMID> --cpu <CPU> --mem <MEMORY> --time <TIME>'
            sys.exit()
        elif opt in ("--cpu", "-cpu"):
            cpu = arg
        elif opt in ("--mem", "-mem"):
            memory = arg
        elif opt in ("--vmid", "-vmid"):
            vmid = arg
        elif opt in ("--time", "-time"):
            time = arg
    
    print subprocess.call("date")
    
    print 'VMID "', vmid
    print 'CPU "', cpu
    print 'memory"', memory
    print 'time"', time

if __name__ == "__main__":
    main(sys.argv[1:])