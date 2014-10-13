#!/bin/bash
targetHostname=$2
ssh-keygen
"id_rsa): "
 if condtion - "Overwrite (y/n)? "
"passphrase): "
"passphrase again: "

"]#"
cd ~/.ssh
"h]#"
chmod 700 ~/.ssh
"h]#"
chmod 600 ~/.ssh/*
"h]#"
ls -ld ~/.ssh & ls -l ~/.ssh
"h]#"
ssh-add
"h]#"
check if target dir exists
ssh root@$targetHostname 'mkdir -p /root/.ssh'
"sword: "
"h]#"
scp /root/.ssh/id_rsa.pub root@$targetHostname:/root/.ssh/authorized_keys
"assword: "
give password
"]# "
ssh root@targetHostname 'chmod 700 /root/.ssh'
"]#"
ssh root@targetHostname 'chmod 600 /root/.ssh/*'


 cat id_rsa.pub | ssh root@node2 "cat >> /root/.ssh/authorized_keys"
