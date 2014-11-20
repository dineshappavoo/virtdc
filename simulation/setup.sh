#!/bin/bash
# path on node1 is /var/lib/virtdc/simulation

# while loop to detect

while [ ! -e /root/task.dat ]
do
sleep 10
done

# iostress needs to gather last min iostat data, let gathering process run first
/usr/bin/python /root/iostress.py -T /root/task.dat >> /root/io.log &

# compile the two files
##/usr/bin/gcc -fopenmp /root/StressCPU.c -o /root/StressCPU
/usr/bin/gcc /root/StressMemory.c -o /root/StressMemory

# Sleep 1 min before start stressing to keep time sync with iostress
sleep 60

##nice -n 19 /root/StressCPU &
##echo $! > /root/cpu.pid

/usr/bin/python /root/simulator.py -T /root/task.dat >> /root/simulator.log &


# echo '' > ~/cpu.pid
# for n in `seq 1 3`
# do
# python ~/square.py &
# echo $! >> ~/cpu.pid
# done
# 
# python ~/simulator.py >> ~/cpu.log &
