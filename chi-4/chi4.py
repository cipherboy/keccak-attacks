#!/usr/bin/env python3

import hash_framework as hf
import itertools, random

from ufds import UFDS

theta = hf.algorithms._sha3.sha3theta
rho = hf.algorithms._sha3.sha3rho
pi = hf.algorithms._sha3.sha3pi
chi = hf.algorithms._sha3.sha3chi
iota = hf.algorithms._sha3.sha3iota

def sha3i(w, x, y, z):
    return w*(5*y + x) + z

def ftheta(w, s):
    ns = [None]*len(s)
    c = {}
    d = {}
    for x in range(0, 5):
        for z in range(0, w):
            c[(x, z)] = s[sha3i(w, x, 0, z)] ^ s[sha3i(w, x, 1, z)] ^ s[sha3i(w, x, 2, z)] ^ s[sha3i(w, x, 3, z)] ^ s[sha3i(w, x, 4, z)]

    for x in range(0, 5):
        for z in range(0, w):
            d[(x, z)] = c[((x - 1) % 5, z)] ^ c[((x + 1) % 5, (z + 1) % w)]

    for x in range(0, 5):
        for y in range(0, 5):
            for z in range(0, w):
                ns[sha3i(w, x, y, z)] = s[sha3i(w, x, y, z)] ^ d[(x, z)]

    return ns


def frho(w, s):
    ns = [None]*len(s)
    for z in range(0, w):
        ns[sha3i(w, 0, 0, z)] = s[sha3i(w, 0, 0, z)]

    x = 1
    y = 0

    for t in range(0, 24):
        for z in range(0, w):
            nz = (z + (t+1)*(t+2)//2)%w
            ns[sha3i(w, x, y, z)] = s[sha3i(w, x, y, nz)]
        x, y = (y, (2*x + 3*y) % 5)

    return ns

def fpi(w, s):
    ns = [None]*len(s)

    for x in range(0, 5):
        for y in range(0, 5):
            for z in range(0, w):
                nx = (x + 3*y) % 5
                ns[sha3i(w, x, y, z)] = s[sha3i(w, nx, x, z)]

    return ns

def fchi(w, s):
    ns = [None]*len(s)

    for x in range(0, 5):
        for y in range(0, 5):
            for z in range(0, w):
                nx1 = (x + 1) % 5
                nx2 = (x + 2) % 5
                ns[sha3i(w, x, y, z)] = s[sha3i(w, x, y, z)] ^ ((not s[sha3i(w, nx1, y, z)]) and s[sha3i(w, nx2, y, z)])

    return ns

def sha3rc(t):
    if (t % 255) == 0:
        return True

    r = [True, False, False, False, False, False, False, False]
    for i in range(1, (t % 255) + 1):
        r = ['F'] + r
        r[0] = r[0] ^ r[8]
        r[4] = r[4] ^ r[8]
        r[5] = r[5] ^ r[8]
        r[6] = r[6] ^ r[8]
        r = r[0:8]

    return r[0]

def sha3RC(w, i):
    RC = [False]*w
    l = int(math.log(w, 2))

    for j in range(0, l+1):
        RC[(1 << j) - 1] = sha3rc(j + 7*i)

    return list(reversed(RC))

def fiota(w, s, i):
    ns = [None]*len(s)

    for x in range(0, 5):
        for y in range(0, 5):
            for z in range(0, w):
                ns[sha3i(w, x, y, z)] = s[sha3i(w, x, y, z)]

    RC = sha3RC(w, i)

    for z in range(0, w):
        ns[sha3i(w, 0, 0, z)] = ns[sha3i(w, 0, 0, z)] ^ RC[z]

    return ns


def sha3r(w, s, r):
    # return iota(w, chi(w, pi(w, rho(w, theta(w, s)))), r)
    return ftheta(w, s)


def random_state(w=1):
    s = ""
    for i in range(0, 25*w):
        if random.randint(0, 1) == 0:
            s += "F"
        else:
            s += "T"

    return s

def flatten(t):
    if type(t) != tuple:
        return t

    if t[0] == 'xor' or t[0] == 'and' or t[0] == 'or':
        r = [t[0]]
        for arg in t[1:]:
            arg_r = flatten(arg)
            if type(arg_r) == tuple and arg_r[0] == r[0]:
                r.extend(arg_r[1:])
            else:
                r.append(arg_r)
        return hf.boolean.simplify(tuple(r))
    elif t[0] == 'not' and type(t[1]) == tuple and t[1][0] == 'xor':
        r = ['xor']
        for arg in t[1:]:
            arg_r = flatten(arg)
            if type(arg_r) == tuple and arg_r[0] == r[0]:
                r.extend(arg_r[1:])
            else:
                r.append(arg_r)
        r[1] = ('not', r[1])
        return hf.boolean.simplify(tuple(r))
    else:
        r = [t[0]]
        for arg in t[1:]:
            arg_r = flatten(arg)
            r.append(arg_r)
        return hf.boolean.simplify(tuple(r))

    return t

# Shows that chi^4 is the identity function
def prove_identity_chi4():
    for w in [1, 2, 4, 8, 16, 32, 64]:
        s = ['i' + str(i) for i in range(0, 25*w)]
        o = chi(w, chi(w, chi(w, chi(w, s))))
        print(w)
        for pos in range(0, len(s)):
            for etvs in itertools.product('TF', repeat=5):
                e_vars = sorted(list(hf.boolean.var_find(o[pos])))
                et = {}
                for i in range(0, len(e_vars)):
                    et[e_vars[i]] = etvs[i]
                ov = hf.boolean.var_eval(o[pos], et)
                assert(ov == et['i' + str(pos)])

# shows that pi^24 is the identity function
def prove_identity_pi24():
    for w in [1, 2, 4, 8, 16, 32, 64]:
        s = ['i' + str(i) for i in range(0, 25*w)]
        o = s.copy()
        for i in range(0, 24):
            o = pi(w, o)
        print(w)
        for pos in range(0, len(s)):
            assert(o[pos] == s[pos])


# shows that rho^w is the identity function
def prove_identity_rho64():
    for w in [1, 2, 4, 8, 16, 32, 64]:
        s = ['i' + str(i) for i in range(0, 25*w)]
        o = s.copy()
        for i in range(0, w):
            o = rho(w, o)
        print(w)
        for pos in range(0, len(s)):
            assert(o[pos] == s[pos])

# shows that theta^(3*w) is the identity function
def prove_identity_theta():
    """
        1  - 3
        2  - 6
        4  - 12
        8  - 24
        16 - 48
        32 - 96
        64 - 192
    """
    for w in [1, 2, 4, 8, 16, 32, 64]:
        count = w * 3
        rounds = ['t']*count

        algo = hf.algorithms.sha3(w=w, rounds=rounds)
        tag = "keccak-attacks-chi4-identity-theta-w" + str(w)

        m = hf.models()
        m.bc_args = []
        m.start(tag, recreate=True)
        hf.models.vars.write_header()
        hf.models.generate(algo, ['h1'], rounds=rounds, bypass=True)
        hf.models.vars.write_assign(['cidentity'])

        cidentity = ['and']
        for i in range(0, 25*w):
            cidentity.append(('equal', 'h1in' + str(i), 'h1out' + str(i)))
        cidentity = ('not', tuple(cidentity))
        hf.models.vars.write_clause('cidentity', cidentity, '01-problem.txt')

        m.collapse()
        m.build()
        res = m.run(count=1)

        if res:
            rg = m.results_generator(algo, prefixes=["h1"])
            count = 0
            for r in rg:
                print(r['h1in'], r['h1out'])
            assert(False)

def to_state(w, i):
    s = [False] * (25*w)
    b = "0" * (25*w)
    b = (b+bin(i)[2:])
    b = b[len(b) - (25*w):len(b)]
    assert(len(b) == (25*w))
    for p in range(0, len(b)):
        if b[p] == '1':
            s[p] = True

    return s

def to_number(w, s):
    assert(len(s) == 25*w)
    ns = []
    for e in s:
        if e:
            ns.append('T')
        else:
            ns.append('F')
    return int(''.join(ns).replace('F', '0').replace('T', '1'), 2)

def find_identity_sha3(w=1, rounds=1):
    print("Creating UFDS data structure...")
    u = UFDS(2**(25*w))

    print("Iterating the range...")
    for i in range(0, 2**(25*w)):
        s = to_state(w, i)
        for r in range(0, rounds):
            s = sha3r(w, s, r)

        j = to_number(w, s)
        u.union(i, j)

        if (i % (2**(25*w) // 100)) == 0:
            print(i)

    print("Generating sizes...")
    u.size(0)
    gs = set()
    inv = {}
    for p in u.sizes:
        s = u.sizes[p]
        gs.add(s)
        inv[s] = inv.get(s, 0) + 1
    # print(u.sizes)
    print(inv)
    print(gs)



# prove_identity_rho64()
# prove_identity_pi24()
# prove_identity_chi4()
# prove_identity_theta()

def profile_func(func):
    import cProfile, pstats
    pr = cProfile.Profile()
    pr.enable()
    func()
    pr.disable()
    sortby = 'cumulative'
    ps = pstats.Stats(pr).sort_stats(sortby)
    ps.print_stats()
    print(hf.boolean.get_simplify_stats())

def a():
    import sys
    assert(len(sys.argv) == 2)
    r = int(sys.argv[1])
    find_identity_sha3(w=1, rounds=r)

profile_func(a)
# a()
