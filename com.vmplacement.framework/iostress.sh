#!/bin/bash

while [ 1 ]
do
    dd if=/dev/zero of=/tmp/test bs=512M count=4 conv=fsync >/dev/null
    echo 3 > /proc/sys/vm/drop_caches
    dd if=/tmp/test of=/dev/null >/dev/null
    echo 3 > /proc/sys/vm/drop_caches
done
