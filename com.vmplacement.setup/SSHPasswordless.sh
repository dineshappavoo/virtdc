#!/bin/bash

if [ "$1" == "" ]; then
    echo "'basename $0' [-h <Remote hostname>] [-u <username to login>] [-p <password to login>]"
    exit 1
fi
 
while [ "$1" != "" ]; 
do
    case $1 in
    -h  )    shift
        REMOTEHOST=$1
        ;;
    -u  )    shift	
        USERNAME=$1
        ;;
    -p  )    shift
        PASSWORD=$1
        ;;
        * )Usage
           exit 1
    esac
    shift
done

#expect 
which expect > /dev/null 2>&1
[[ "$?" != "0" ]] && echo "[ERROR] 'expect' not found." && exit 1
 

[[ "$REMOTEHOST" == "" ]] && echo "[ERROR] -h option is required." && exit 1
[[ "$USERNAME" == "" ]] && echo "[ERROR] -u option is required. " && exit 1
[[ "$PASSWORD" == "" ]] && echo "[ERROR] -p option is required. " && exit 1
 
ID_RSA="$HOME/.ssh/id_rsa.pub"
 
#check remote host ~/.ssh dir
cmd="ssh $USERNAME@$REMOTEHOST ls ~/.ssh"
expect <<- DONE
  spawn $cmd
  expect {
      "*yes/no*"    { send "yes\r"; exp_continue }
      "*password*"  { send "$PASSWORD\r" ; exp_continue}
  }
 
DONE
 
[[ "$?" == "255" ]] && echo "[ERROR] Failed to login, please check if the given username and password are correct." && exit 1

if [ "$?" != "0" ]; then


cmd="ssh $USERNAME@$REMOTEHOST mkdir .ssh"
expect <<- DONE
  spawn $cmd
  expect {
      "*yes/no*"    { send "yes\r"; exp_continue }
      "*password*"  { send "$PASSWORD\r" ; exp_continue}
  }
 
DONE
 

 
cmd="ssh $USERNAME@$REMOTEHOST touch .ssh/authorized_keys"
expect <<- DONE
  spawn $cmd
  expect {
      "*yes/no*"    { send "yes\r"; exp_continue }
      "*password*"  { send "$PASSWORD\r" ; exp_continue}
  }
 
DONE
 
fi


#Generate SSH key
cmd="ssh-keygen"
expect <<- DONE
  spawn $cmd
  expect {
      "/id_rsa): "  	{ send "\r"; exp_continue }
      "verwrite (y/n)? " { send "n\r"; exp_continue }
      "ssphrase): " 	{ send "\r"; exp_continue }
      "ssphrase again: " { send "\r"; exp_continue }
  }

DONE

#SSH_ADD
cmd="ssh-add"
expect <<- DONE
  spawn $cmd
  expect {

  }
 
DONE

cmd="chmod 700 ~/.ssh"
expect <<- DONE
  spawn $cmd
  expect {
      "*yes/no*"    { send "yes\r"; exp_continue }
      "*password*"  { send "$PASSWORD\r" ; exp_continue}
  }
 
DONE

cmd="chmod 600 ~/.ssh/*"
expect <<- DONE
  spawn $cmd
  expect {
      "*yes/no*"    { send "yes\r"; exp_continue }
      "*password*"  { send "$PASSWORD\r" ; exp_continue}
  }
 
DONE

#scp id_rsa.pub to remote host
cmd="scp $ID_RSA $USERNAME@$REMOTEHOST:/root/.ssh/id_rsa-`hostname`.pub"
expect <<- DONE
  spawn $cmd
  expect {
      "*yes/no*"    { send "yes\r"; exp_continue }
      "*assword*"  { send "$PASSWORD\r" ; exp_continue}
  }
 
DONE
 
[[ "$?" != "0" ]] && echo "[ERROR] Failed to scp $ID_RSA to remote host." && exit 1
 
cmd="ssh $USERNAME@$REMOTEHOST cat ~/.ssh/id_rsa-`hostname`.pub >> ~/.ssh/authorized_keys"
expect <<- DONE
  spawn $cmd
  expect {
      "*yes/no*"    { send "yes\r"; exp_continue }
      "*password*"  { send "$PASSWORD\r" ; exp_continue}
  }
 
DONE

cmd="ssh $USERNAME@$REMOTEHOST chmod 700 ~/.ssh"
expect <<- DONE
  spawn $cmd
  expect {
      "*yes/no*"    { send "yes\r"; exp_continue }
      "*password*"  { send "$PASSWORD\r" ; exp_continue}
  }
 
DONE

[[ "$?" != "0" ]] && echo "[ERROR] Failed to append id_rsa to remote host." && exit 1
 
cmd="ssh $USERNAME@$REMOTEHOST chmod 600 ~/.ssh/*"
expect <<- DONE
  spawn $cmd
  expect {
      "*yes/no*"    { send "yes\r"; exp_continue }
      "*password*"  { send "$PASSWORD\r" ; exp_continue}
  }
 
DONE
 
ssh $USERNAME@$REMOTEHOST ls > /dev/null 2>&1
 
[[ "$?" != "0" ]] && echo "[ERROR] passwordless login setup failed." && exit 1
echo "Passwordless ssh from `hostname` to $REMOTEHOST established."
