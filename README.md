VM Placement and Scaling
=======================

Statically place and schedule and dynamically scale and migrate Vitual Machines (VMs) to optimize resource utilization by using efficient VM algorithms while meeting the SLAs of users in cloud

##Install

###Build the VM framework
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

###Build the VM placement manager
* Design and develop a VM placement, scaling, and migration decision algorithm 
* Implement the placement manager based on the algorithm
* Placement manager for dynamic VM placement changes
* Invoke (VM_workload) periodically to obtain VM workload data for all VMs 
* Invoke (VM_terminationList) periodically to obtain the list of terminated jobs
* Decide whether there should be VM scaling or VM migration. If so, make the decision 
* Invoke (VM_change_placement) to give the decision and activate changes
* Placement manager for new job placement
* Implement an API to give placement decision for a new job (place_newJob)
* Analyze and decide where to place the VMs
* Return the placement decision to VM framework

### Build the simulation framework
* Take Google cloud traces, extract the workload information
* Explore various application programs for benchmarking
* Take each job in Google data to obtain input workload, use appropriate benchmarks to simulate the input workload
* One job may have multiple tasks, make sure it is simulated the same way
* Introduce some degree of errors in the workload
* Also simulate the job issuing time (from Google data)
* Issue the job when time is right
* Invoke (VM_submitJob) to submit the job
* Activate an event listener to listen to the (job_termination_event)
* When the event is triggered, invoke (VM_jobReport) to get the execution information and output of the job
* Let the system run, obtain the performance results and analyze them
* If possible, try to alter the VM placement algorithm and see how system behavior changes
* Need to workout the specific parameters for each API
* All interactions should be standardized so that they can interoperate

##Project Contributor

* Dinesh Appavoo ([@DineshAppavoo](https://twitter.com/DineshAppavoo))
