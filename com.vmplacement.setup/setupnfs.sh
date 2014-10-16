#!/usr/bin/sh
mkdir -p /exports/images
cat >>/etc/exports <<EOF
/exports/images    192.168.122.0/24(rw,no_root_squash)
EOF
exportfs -a
systemctl restart nfs-server.service
systemctl status nfs-server.service

#cat >>/etc/fstab <<EOF
#node1:/exports/images  /var/lib/libvirt/images  nfs  auto  0 0
#EOF
#mount /var/lib/libvirt/images

