#!/usr/bin/bash
########################
# On NFS server (node1)
########################
mkdir /home/nfs
mkdir /home/vm_img
cat >>/etc/exports <<EOF
/home/nfs node1(rw,sync,no_root_squash) node2(rw,sync,no_root_squash) node3(rw,sync,no_root_squash) node4(rw,sync,no_root_squash)
EOF
exportfs -a
systemctl stop firewalld
systemctl restart nfs-server.service
systemctl status nfs-server.service
mount node1:/home/nfs /home/vm_img
setsebool -P virt_use_nfs on
getsebool virt_use_nfs

