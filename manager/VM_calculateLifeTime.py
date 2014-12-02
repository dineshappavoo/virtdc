#!/usr/bin/python


import sys, math, csv, time, datetime

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

data_folder_path='/var/lib/virtdc/data/vms'

def calculate_vm_lifetime(file_name):
        ifile  = open(file_name, "rt")
        reader = csv.reader(ifile)
        total_time=0
        last=0
        #prevLast=0
        for row in reader:
                #secprevLast = prevLast
                prevLast = last
                last=int(row[0].partition(" ")[0])
                total_time = total_time + last
        total_time=total_time-last-prevLast #-secprevLast
        ifile.close()
        return total_time

def calculate_vm_endtime(vm_id, start_time):
        lifetime = calculate_vm_lifetime(data_folder_path+"/"+vm_id+".csv")
	start = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S.%f")
        #print 'START Time-' + str(time.mktime(start.timetuple()))
        #print 'Lifetime - '+ str(lifetime)
        end_time = lifetime+ time.mktime(start.timetuple())
        #print "END Time" +str(end_time)
        return end_time
    	

if __name__ == "__main__":
	while(1):	
		end = calculate_vm_endtime('VM_Task_26', str(datetime.datetime.now()))
		current_time= time.time()
		#print 'Current Time-'+ str(current_time)
		#print 'Time '+str(time.time())
		if(current_time>=end):
			print 'terminate'
		time.sleep(20)
