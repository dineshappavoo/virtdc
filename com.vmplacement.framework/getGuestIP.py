#!/usr/bin/python

'''
This script use pexpect module to interactively login guest VM
and return its IP address
'''

import pexpect

vmid = "Test_node1"
username = "root"
password = "Teamb@123"

child = pexpect.spawn('/usr/bin/virsh console ' + vmid)
child.sendline('\n\n')
child.expect('ogin: ')
child.sendline(username)
child.expect('assword:')
child.sendline(password)
child.expect(']# ')
child.sendline('ifconfig | grep 192.168 | awk \'{print $2}\'')
child.expect('(\d+\.\d+\.\d+\.\d+)')
ip = child.match.group()
child.sendline('logout')

print ip
