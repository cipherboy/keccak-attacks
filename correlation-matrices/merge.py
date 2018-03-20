#!/usr/bin/env python3

import json, sys
import numpy

print(sys.argv)

print("Loading a...")
a = json.load(open(sys.argv[1], 'r'))
print("Done")
print("Loading b...")
b = json.load(open(sys.argv[2], 'r'))
print("Done")
out_f = open(sys.argv[3], 'w')

a_e_set = set()
b_e_set = set()

print("Analyzing overlap...")
for e in a[0]:
    a_e_set.add(tuple(e))

for e in b[0]:
    b_e_set.add(tuple(e))

common = len(a_e_set.intersection(b_e_set))
print("Done")

if common != 0 and len(sys.argv) == 4:
    print("FIles have " + str(common) + " common entries. Refusing to continue unless --force flag is passed.")
    sys.exit(1)

print("Beginning merge...")

a[0] += b[0]
n = len(a[1])
for k in range(1, 6):
    a[k] = numpy.add(a[k], b[k]).tolist()

print("Done")
print("Writing...")
json.dump(a, out_f)


if not out_f.closed:
    out_f.flush()
    out_f.close()

print("Done")
