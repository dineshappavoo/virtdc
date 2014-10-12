#!/bin/bash
echo '' > ~/cpu.pid
for n in `seq 1 3`
do
python ~/square.py &
echo $! >> ~/cpu.pid
done

python ~/simulator.py >> ~/cpu.log &
