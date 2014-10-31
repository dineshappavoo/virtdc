#!/bin/bash
if [ -e /root/io.pid ]
then
    rm -f /root/io.pid
fi

while [ 1 ]
do
    nice -n 19 dd if=/dev/zero of=/tmp/test bs=4K count=131072 conv=fsync 2>/dev/null && rm -f /root/io.pid &
    echo $! > /root/io.pid
    while [ -e /root/io.pid ]
    do
    	sleep 5
    done
    echo 3 > /proc/sys/vm/drop_caches
    rm -f /root/io.pid
    nice -n 19 dd if=/tmp/test of=/dev/null 2>/dev/null && rm -f /root/io.pid &
    echo $! > /root/io.pid
    while [ -e /root/io.pid ]
    do
	sleep 5
    done
    echo 3 > /proc/sys/vm/drop_caches
    rm -f /root/io.pid
done
