#!/usr/bin/env python3

import json, sys

raw_data = json.load(open(sys.argv[1], 'r'))

entries = len(raw_data[0])
print("Number of entries")
print(entries)

d = []
for i in range(0, 9*8):
    for j in range(0, 9*8):
        if i == j:
            continue
        if raw_data[4][i][j] < (entries/4):
            d.append(('-', i, j, raw_data[4][i][j]))
        elif raw_data[4][i][j] > (3*entries/4):
            d.append(('+', i, j, raw_data[4][i][j]))

print("Anomalies in entries")
print(len(d))
d = []
l = len(raw_data[4])
mik = 3*entries/16
mak = 13*entries/16

print("Entries above " + str(mak) + " or below " + str(mik))
for i in range(0, l):
    for j in range(i+1, l):
        for k in range(1, 6):
            if i == j or (i < 200 and j < 200) or (i < 200 and k < 3):
                continue
            if raw_data[k][i][j] < mik:
                d.append(('-', i, j, k, raw_data[k][i][j]))
                print(d[len(d) - 1])
            elif raw_data[k][i][j] > mak:
                d.append(('+', i, j, k, raw_data[k][i][j]))
                print(d[len(d) - 1])

print("Number of such entries")
print(len(d))

for k in range(1, 6):
    min_v = entries*2
    min_p = []
    max_v = 0
    max_p = []
    for i in range(0, l):
        for j in range(i+1, l):
            if i == j or (i < 200 and j < 200) or (i < 200 and k < 3):
                continue
            if raw_data[k][i][j] > max_v:
                max_v = raw_data[k][i][j]
                max_p = (i, j)
            if raw_data[k][i][j] < min_v:
                min_v = raw_data[k][i][j]
                min_p = (i, j)
    print("Min value for k=" + str(k))
    print((min_v, min_p))
    print("Max value for k=" + str(k))
    print((max_v, max_p))


