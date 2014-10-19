#!/bin/bash
# path on node1 is /home/cloud/VMPlacementAndScaling/com.vmplacement.framework/vms

# while loop to detect

while [ ! -e /root/task.dat ]
sleep 10
done

# compile the two files
gcc -fopenmp /root/StressCPU.c -o cpu
gcc /root/StressMemory.c -o memory

sleep 60
# echo '' > ~/cpu.pid
# for n in `seq 1 3`
# do
# python ~/square.py &
# echo $! >> ~/cpu.pid
# done
# 
# python ~/simulator.py >> ~/cpu.log &
