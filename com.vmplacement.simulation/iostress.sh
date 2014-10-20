#!/bin/bash
if [ -e /root/io.pid ]
then
    rm -f /root/io.pid
fi

while [ 1 ]
do
    dd if=/dev/zero of=/tmp/test bs=512M count=4 conv=fsync >/dev/null && rm -f /root/io.pid &
    echo $! > /root/io.pid
    while [ -e /root/io.pid ]
    do
    	sleep 5
    done
    echo 3 > /proc/sys/vm/drop_caches
    rm -f /root/io.pid
    dd if=/tmp/test of=/dev/null >/dev/null && rm -f /root/io.pid &
    echo $! > /root/io.pid
    while [ -e /root/io.pid ]
    do
	sleep 5
    done
    echo 3 > /proc/sys/vm/drop_caches
    rm -f /root/io.pid
done
