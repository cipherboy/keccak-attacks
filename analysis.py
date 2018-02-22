#!/usr/bin/env python3

import json, sys

raw_data = json.load(open(sys.argv[1], 'r'))

entries = len(raw_data[0])
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

d = []
l = len(raw_data[4])
for i in range(200, l):
    for j in range(200, l):
        for k in range(1, 6):
            if i == j:
                continue
            if raw_data[k][i][j] < (entries/16):
                d.append(('-', i, j, k, raw_data[k][i][j]))
                print(d[len(d) - 1])
            elif raw_data[k][i][j] > (15*entries/16):
                d.append(('+', i, j, k, raw_data[k][i][j]))
                print(d[len(d) - 1])



print(len(d))
