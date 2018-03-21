import hash_framework as hf
from hash_framework.boolean import *

import random, itertools, sys
from functools import partial

def sha3i(w, x, y, z):
    return w*(5*y + x) + z

def sha3ri(w, x, z):
    return w*x + z

def sha3rir(w, p):
    z = p % w
    x = (p - z) // w

    return (x, z)

def sha3r(w, p):
    z = p % w
    r = p // w
    x = r % 5
    r = r // 5
    y = r
    return (x, y, z)

rtheta = hf.algorithms._sha3.sha3theta

def random_state(w=1):
    s = ""
    for i in range(0, 25*w):
        if random.randint(0, 1) == 0:
            s += "F"
        else:
            s += "T"

    return s

for w in [1, 2, 4, 8, 16, 32, 64]:
    for tpos in range(0, 25*w):
        s = ['F']*(25*w)
        s[tpos] = 'T'
        os = rtheta(w, s)
        assert(os.count('T') == 11)
