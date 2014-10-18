#!/usr/bin/sh
########################
# On NFS server (node1)
########################
mkdir /home/nfs
mkdir /home/vm_img
cat >>/etc/exports <<EOF
/home/nfs node1(rw,sync,no_root_squash) node2(rw,sync,no_root_squash) node3(rw,sync,no_root_squash) node4(rw,sync,no_root_squash)
EOF
exportfs -a
systemctl restart nfs-server.service
systemctl status nfs-server.service
mount node1:/home/nfs /home/vm_img
setsebool -P virt_use_nfs on
getsebool virt_use_nfs

#################
# On NFS Clients
#################
systemctl restart nfs-server.service
systemctl status nfs-server.service
mkdir /home/vm_img
mount node1:/home/nfs /home/vm_img
setsebool -P virt_use_nfs on
getsebool virt_use_nfs


#cat >>/etc/fstab <<EOF
#node1:/exports/images  /var/lib/libvirt/images  nfs  auto  0 0
#EOF
#mount /var/lib/libvirt/images

