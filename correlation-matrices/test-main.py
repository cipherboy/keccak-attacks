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

def check_matrix(states, raw_data):
    n = len(states)
    m = []
    ne = {0: 1, 1: 0}
    for i in range(0, n):
        m.append([0] * n)
    for i in range(0, n):
        for j in range(0, n):
            a = states[i]
            b = states[j]
            na = ne[a]
            nb = ne[b]
            if (a & b) != raw_data[1][i][j]:
                print(("a and b", i, j))
                assert(False)
            if (a & nb) != raw_data[2][i][j]:
                print(("a and not b", i, j))
                assert(False)
            if (na & b) != raw_data[3][i][j]:
                print(("not a and b", i, j))
                assert(False)
            if (a ^ b) != raw_data[4][i][j]:
                print(("a xor b", i, j))
                assert(False)
            if (a | b) != raw_data[5][i][j]:
                print(("a or b", i, j))
                assert(False)

assert(len(raw_data[0]) == 1)
states = to_binary(raw_data[0][0])
check_matrix(states, raw_data)
