VM Placement and Scaling
=======================

Statically place and schedule and dynamically scale and migrate Vitual Machines (VMs) to optimize resource utilization by using efficient VM algorithms while meeting the SLAs of users in cloud

##Install

###Build the VM framework - com.framework.python
* Set up the KVM environment, explore VM creation
* Explore libvirt to achieve VM scaling and VM migration
* Activate a monitoring system, can be Ganglia or just collect data from logs, to report    VM workload information
* Implement an API to accept VM placement change decisions (VM_change_placement)
* Based on the decision, perform VM scaling, VM migration
* Implement an API to accept job submission (VM_submitJob)
* Extract job information for placement decision
* Invoke (place_newJob) to get a placement decision
* Create the VMs at the corresponding host
* Implement a mechanism to notify the client the (job_termination_event)
* Implement an API to report the results of a job execution (VM_jobReport)
* Implement an API for VM workload data provisioning (VM_workload)
* Implement an API for VM termination notification (VM_terminationList)
* Keep good logs to record the job execution characteristics, the placement decisions and changes,etc. for performance analysis of the VM placement algorithm

###Impacted Files and Information
* __Host_machine_info_tracker.py__ - Tracks available hardware on the host machine and maintains in memory
* __VM_submitJob.py__ - Accept a new job and create new VM with the job configuration based on the availability of hardware
* __VM_decisionMaker.py__ - makes the decision to find the right place for the new VM for the first time
* __nodeinfo.xml__ - Maintains the host hardware information in the XML format
* __guestconfig.xml__ - dump XML (with replaceable keywords for future new VM’s) of the base VM which will be used to clone new VM’s
* __references.txt__ - Maintains the referrences


##Project Contributors

* Dinesh Appavoo ([@DineshAppavoo](https://twitter.com/DineshAppavoo))
* Ryan Wang
* Rahul Nair
* Qinghao Dai
* Haan Mo Johng
