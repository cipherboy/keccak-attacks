#!/bin/bash


./build.sh

num_process=`cat /proc/cpuinfo | grep 'processor' | wc -l`
job_tmp="$HOME/keccak-attacks-tmp"

mkdir -p $job_tmp

for i in `seq 1 $num_process`; do
    ./bin/matrix > $job_tmp/m$i.txt &
done
wait

echo "Done waiting"

python3 merge.py $job_tmp/m1.txt $job_tmp/m2.txt $job_tmp/merged.txt
rm $job_tmp/m1.txt $job_tmp/m2.txt

for i in `seq 3 $num_process`; do
    python3 merge.py $job_tmp/m$i.txt $job_tmp/merged.txt $job_tmp/merged.txt
    rm $job_tmp/m$i.txt
done

