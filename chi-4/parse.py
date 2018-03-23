import json, sys
from math import gcd
a = [100, 200, 150]   #will work for an int array of any length

def lcm(a):
    r = a[0]
    for i in a[1:]:
        r = r*i//gcd(r, i)
    return r

obj = json.load(open(sys.argv[1], 'r'))
print(len(obj['fixed_points']) - 1)
if len(obj['fixed_points']) < 30 and len(obj['fixed_points']) > 1:
    for f in obj['fixed_points']:
        if f == -1:
            continue
        print("\t", f)

print(obj['cycles'])

cycles = {}
for k in obj['cycle_map']:
    v = obj['cycle_map'][k]
    if v == -1 or k == "-1":
        continue

    if not v in cycles:
        cycles[v] = set()

    cycles[v].add(k)

for k in cycles:
    cycles[k] = len(cycles[k])

print(cycles)
print(set(cycles))
print(lcm(list(set(cycles))))
