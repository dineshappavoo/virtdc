#!/bin/bash
# path on node1 is /home/cloud/VMPlacementAndScaling/com.vmplacement.framework/vms

# while loop to detect

while [ ! -e /root/task.dat ]
do
sleep 10
done

# compile the two files
gcc -fopenmp /root/StressCPU.c -o /root/cpu
gcc /root/StressMemory.c -o /root/memory

/root/cpu &
echo $! > /root/cpu.pid

python /root/simulator.py -T /root/task.dat >> /root/simulator.log &

/root/iostress.sh > /dev/null &

sleep 30

python /root/iostress.py -T /root/task.dat >> /root/io.log &

# echo '' > ~/cpu.pid
# for n in `seq 1 3`
# do
# python ~/square.py &
# echo $! >> ~/cpu.pid
# done
# 
# python ~/simulator.py >> ~/cpu.log &
