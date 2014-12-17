#!/usr/bin/env python
import subprocess, os

def kill_after_terminate():
    proc_to_kill_1 = "VM_terminationHandler"
    proc_to_kill_2 = "vmonere_listener.socket"
    proc_to_kill_3 = "vmonere_log_deleter"

    kill_array = list()
    kill_array.append(proc_to_kill_1)
    kill_array.append(proc_to_kill_2)
    kill_array.append(proc_to_kill_3)
    
    for name in kill_array:
        cmd = "/usr/bin/ps -ef | /usr/bin/grep %s | grep -v 'grep' | /usr/bin/head -1 | /usr/bin/awk '{print $2}'" % name
        pid = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
        pid = int(pid.strip())
        os.system("/usr/bin/kill -9 %s" % pid)

    os.system("/usr/bin/rm -f /var/lib/virtdc/framework/node_dict.pkl")
    os.system("/usr/bin/rm -f /var/lib/virtdc/framework/host_vm_dict.pkl")
    os.chdir("/var/lib/virtdc/framework")
    os.system("/var/lib/virtdc/framework/Host_Info_Tracker.py")


if __name__ == "__main__":
    kill_after_terminate()
