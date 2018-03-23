#!/bin/bash

r=1
for f in t r p c tr rp trp rpc trpc; do
    python3 -u ./chi4.py $r $f | tee ufds-w1-r$r-f$f.txt &
done
wait


for f in ci pci rpci trpci; do
    for r in `seq 1 24`; do
        python3 -u ./chi4.py $r $f | tee ufds-w1-r$r-f$f.txt &
    done
    wait
done
