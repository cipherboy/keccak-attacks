#!/usr/bin/env python3

import json, sys

raw_data = json.load(open(sys.argv[1], 'r'))

def to_binary(elm):
    b = ""
    for c in elm:
        z = bin(c)[2:]
        while len(z) < 8:
            z = "0" + z
        b += z
    return list(map(int, list(b)))

t_matrix = [0]*len(raw_data[0][0])
f_matrix = [0]*len(raw_data[0][0])

for entry in raw_data[0]:
    b = to_binary(entry)
    while len(f_matrix) < len(b):
        f_matrix.append(0)
    while len(t_matrix) < len(b):
        t_matrix.append(0)
    for i in range(0, len(b)):
        if b[i] == 0:
            f_matrix[i] += 1
        else:
            t_matrix[i] += 1

print(t_matrix)
print(f_matrix)
