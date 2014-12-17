#!/usr/bin/env python

import time
import sys
import datetime
sys.path.append('/var/lib/virtdc/manager')
sys.path.append('/var/lib/virtdc/framework')
from VM_PlacementManager import report_usage_to_placement_manager

import socket               # Import socket module

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

#domain_dict = {}

def start_server():

	domain_dict = {}			#Maintain the dictionary to count the domain report frequency. It will be helpful to report usage to placement manager

	   
	s = socket.socket()			# Create a socket object
	host = socket.gethostname()		# Get local machine name
	port = 12345				# Reserve a port for your service.
	s.bind((host, port))        		# Bind to the port

	s.listen(15)                 		# Now wait for client connection.


	while True:
		c, addr = s.accept()		# Establish connection with client.
		#print 'Got connection from', addr
		#c.send('Thank you for connecting')
		
		usage = c.recv(1024)

		try:
			#Activity Log
			vmlistener_log = open('/var/lib/virtdc/logs/activity_logs/vmlistener.log', 'a+')
			usage = usage.strip()
			guest_usage = usage.split('|')
			vmid = guest_usage[0].strip() if len(guest_usage[0].strip()) != 0 else 0
			cpu_usage = guest_usage[1].strip() if len(guest_usage[1].strip()) != 0 else 0
			os_mem_usage = guest_usage[2].strip() if len(guest_usage[2].strip()) != 0 else 0
			task_mem_usage = guest_usage[3].strip() if len(guest_usage[3].strip()) != 0 else 0
			io_usage = guest_usage[4].strip() if len(guest_usage[4].strip()) != 0 else 0


			path = '/var/lib/virtdc/vmonere/monitor_logs/domain/'+vmid+'.log'
			file= open(path, 'a+')
            		time_now = str(datetime.datetime.now())
			usage=  time_now +' \t|\t '+ vmid+' \t|\t '+ str(cpu_usage) +  '\t|\t' + str(task_mem_usage) + '\t|\t' + str(io_usage) + '\t|\t' + str(os_mem_usage) 
			file.write(usage+'\n')
			file.close()

			report_usage_to_placement_manager(vmid, cpu_usage, task_mem_usage, io_usage)		# Report the usage every 30 seconds [6 * 5s interval]

			'''
            #To log usage in json file
            log_usage_json(vmid, time_now, cpu_usage, task_mem_usage, io_usage)
            '''
                
			#To report current usage to the placement manager
			domain_reported_count = domain_dict[vmid]
			if domain_reported_count is None:
				domain_dict[vmid] = 1
			elif (domain_reported_count >= 6):
				report_usage_to_placement_manager(vmid, cpu_usage, task_mem_usage, io_usage)		# Report the usage every 30 seconds [6 * 5s interval]
				domain_dict[vmid] = 0
			else:
				domain_dict[vmid] = (domain_reported_count + 1)
			


		except Exception as e:
			vmlistener_log.write(str(datetime.datetime.now()) +' :: vmonere listener :: '+vmid+' :: error in listener / reporting to manager \n')
			vmlistener_log.write(str(e) + '\n')
			pass

		#print usage

		c.close()                # Close the connection

def log_usage_json(vmid, time_now, cpu, mem, io):
	#is_domain_exist = domain_dict[vmid]
    
    path = '/var/lib/virtdc/vmonere/monitor_logs/domain/json/' + vmid + '.json'


    with open(path) as log_file:
        dict = json.load(log_file)
    print log_dict

    dict["time"] = time_now
    dict["cpu"] = cpu
    dict["memory"] = mem
    dict["io"] = io
    

    with open(path,"w") as f:
        json.dump(dict,f)


if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   start_server()
