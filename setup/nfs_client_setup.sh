#!/usr/bin/bash
#################
# On NFS Clients
#################
systemctl stop firewalld
systemctl restart nfs-server.service
systemctl status nfs-server.service
mkdir /home/vm_img || true
mount node1:/home/nfs /home/vm_img || true
setsebool -P virt_use_nfs on
getsebool virt_use_nfs

