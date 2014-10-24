#!/usr/local/bin/python


import sys
import math
import csv

def calculate_vm_lifetime(file_name):
        ifile  = open(file_name, "rt")
        reader = csv.reader(ifile)
        total_time=0
        last=0
        for row in reader:
                prevLast = last
                last=int(row[0].partition(" ")[0])
                total_time = total_time + last
        total_time=total_time-last-prevLast
        sys.stdout.write("Final Total Time: %d   \r" % (total_time) )
        ifile.close()
        return total_time
        	

if __name__ == "__main__":
    calculate_vm_lifetime("VM_Task_1.csv")			
