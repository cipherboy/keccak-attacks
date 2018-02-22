#!/bin/bash


./build.sh

num_processes=4
job_tmp="$HOME/keccak-attacks-tmp"

mkdir -p $job_tmp

for i in `seq 1 $num_process`; do
    ./bin/matrix > $job_tmp/m$i.txt &
done
wait

echo "Done waiting"

python3 merge.py $job_tmp/m3.txt $job_tmp/m4.txt $job_tmp/mm2.txt &
python3 merge.py $job_tmp/m1.txt $job_tmp/m2.txt $job_tmp/mm1.txt &
wait
rm $job_tmp/m1.txt $job_tmp/m2.txt $job_tmp/m3.txt $job_tmp/m4.txt

python3 merge.py $job_tmp/mm1.txt $job_tmp/mm2.txt $job_tmp/merged.txt
rm $job_tmp/mm1.txt $job_tmp/mm2.txt

