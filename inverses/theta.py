import hash_framework as hf
from hash_framework.boolean import *

import random, itertools, sys
from functools import partial
from invmap import *

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

def theta(w=1):
    C = []
    D = []
    for i in range(0, 5):
        C.append([None] * w)
        D.append([None] * w)

    for x in range(0, 5):
        for z in range(0, w):
            C[x][z] = set([(x, 0, z), (x, 1, z), (x, 2, z), (x, 3, z), (x, 4, z)])

    for x in range(0, 5):
        for z in range(0, w):
            D[x][z] = C[(x - 1) % 5][z] ^ C[(x+1) % 5][(z+1)%w]

    A = []
    for x in range(0, 5):
        a = []
        for y in range(0, 5):
            a.append([None] * w)
        A.append(a)

    for x in range(0, 5):
        for y in range(0, 5):
            for z in range(0, w):
                A[x][y][z] = set([(x, y, z)]) ^ D[x][z]

    return A

def inv_map_to_bin(w):
    inv_map = get_invmap(w)
    for i in range(0, w):
        s = ['0'] * (5*w)
        for p in inv_map[i]:
            s[p] = '1'
        print(int(''.join(s), 2))

def theta_inverse(w, s):
    r = ['F'] * len(s)
    inv_map = get_invmap(w)

    assert(len(inv_map) != 0)
    C = []
    Dp = []
    for i in range(0, 5):
        C.append([None] * w)
        Dp.append([None] * w)

    for x in range(0, 5):
        for z in range(0, w):
            C[x][z] = b_xor(b_xor(b_xor(s[sha3i(w, x, 0, z)], s[sha3i(w, x, 1, z)]), s[sha3i(w, x, 2, z)]), b_xor(s[sha3i(w, x, 3, z)], s[sha3i(w, x, 4, z)]))

    for x in range(0, 5):
        for z in range(0, w):
            Dv = None
            p = sha3ri(w, x, z)
            for loc in inv_map[p]:
                lx, lz = sha3rir(w, loc)
                if Dv == None:
                    Dv = C[lx][lz]
                else:
                    Dv = b_xor(Dv, C[lx][lz])

            assert(Dv != None)
            Dp[x][z] = Dv

    for x in range(0, 5):
        for y in range(0, 5):
            for z in range(0, w):
                p = sha3i(w, x, y, z)
                r[p] = b_xor(s[p], Dp[x][z])

    return r


def rtheta_inverse(w, s):
    algo = hf.algorithms.sha3(w=w, rounds=['t'])
    tag = "keccak-attacks-theta-inverse"

    m = hf.models()
    m.start(tag, recreate=True)
    hf.models.vars.write_header()
    hf.models.generate(algo, ['h1'], rounds=['t'], bypass=True)
    hf.models.vars.write_assign(['cinput', 'coutput'])

    #cinput = ['and']
    #for i in range(0, 25*w):
    #    cinput.append(('equal', 'h1in' + str(i), 'T'))
    #cinput = tuple(cinput)
    #hf.models.vars.write_range_clause('cinput', input_differences, input_differences, cinput, '50-input.txt')

    coutput = ['and']
    for i in range(0, 25*w):
        coutput.append(('equal', 'h1out' + str(i), s[i]))
    coutput = tuple(coutput)
    hf.models.vars.write_clause('coutput', coutput, '50-output.txt')

    m.collapse()
    m.build()
    m.run(count=10000)

    rg = m.results_generator(algo, prefixes=["h1"])
    for r in rg:
        print(r['h1in'])

    return r['h1in']

    return None



def cpfind(s=None, w=1):
    if s == None:
        s = random_state(w)

    ns = rtheta(w, s)
    count = 1
    while ns != s:
        ns = rtheta(w, ns)
        count += 1
        if count % 1000 == 0:
            print(count)

    return count

def check(func, w=1):
    for x in range(0, 5):
        for y in range(0, 5):
            for z in range(0, w):
                if not func(w, x, y, z):
                    # print((w, x, y, z))
                    return False
    return True

def locs(A, w=1):
    graph = {}
    for x in range(0, 5):
        for y in range(0, 5):
            for z in range(0, w):
                 for elm in A[x][y][z]:
                    if not elm in graph:
                        graph[elm] = set()
                    graph[elm].add((x, y, z))
    return graph

def flatten(A, w=1):
    arr = [None]*(25*w)
    for x in range(0, 5):
        for y in range(0, 5):
            for z in range(0, w):
                arr[sha3i(w, x, y, z)] = A[x][y][z]

    return arr

def d_xor(f, ps):
    a = None
    for p in ps:
        if a == None:
            a = f[p]
        else:
            a = a ^ f[p]
    return a

def d_cxor(f, ips):
    ps = []
    w = len(f)//25
    print(w)
    for ip in ips:
        ps.append(sha3i(w, ip[0], ip[1], ip[2]))
    print(ps)
    return d_xor(f, ps)

def d_ixor(f, ps):
    w = len(f)//25
    return m_itop(w, d_xor(f, ps))

def d_add(s, p):
    print(s, p)
    x, y, z = list(s)[0]
    loc = sha3i(w, x, y, z)
    return loc

def a(f, w, ox, oy, oz, sz1, sz2, sx1, sx2):
    xp = (ox + sx1) % 5
    xpp = (ox + sx2) % 5

    cp = [(ox, oy, oz)]
    for ny in range(0, 5):
        for nz in sz1:
            cp.append((xp, ny, nz % w))

        for nz in sz2:
            cp.append((xpp, ny, nz % w))

    p = list(map(lambda a: sha3i(w, a[0], a[1], a[2]), cp))

    r = d_xor(f, p)
    # if not (len(r) == 1 or list(r)[0] == (x, y, z)):
    #     print((w, (x, y, z), len(r), sorted(cp), sorted(p)))

    return len(r) == 1 and list(r)[0] == (ox, oy, oz)

def d_pgen(s):
    p = []
    for i in range(0, len(s)):
        if s[i] == "T":
            p.append(i)
    return tuple(p)

def d_sgen(w, poses):
    s = ['F'] * 25*w
    for pos in poses:
        s[pos] = 'T'
    return s

def d_spgen(w, pos):
    s = d_sgen(w, [pos])
    ns = rtheta(w, s)
    return set(d_pgen(ns))

def d_aspgen(w):
    res = {}
    for i in range(0, 25*w):
        res[i] = d_spgen(w, i)
    return res

def m_itop(w, inds):
    return sorted(list(map(lambda x: sha3i(w, x[0], x[1], x[2]), inds)))

def d_cps(w, x):
    return [x, (5*w)+x, (10*w)+x, (15*w)+x, (20*w)+x]


def d_pxor(f, t, poses):
    nset = None
    for pos in poses:
        if nset == None:
            nset = t[pos]
        else:
            nset = nset ^ t[pos]

    # print(nset)
    xor_out = d_xor(f, nset)
    if xor_out == None:
        return []
    return m_itop(w, xor_out)
    #print()
    #print(len(xor_out))

    # return len(xor_out) == 1

def check_perm(Af, w, p, l):
    ps = [l]
    for e in p:
        ps = ps + d_cps(w, e)
    xor_out = d_xor(Af, ps)
    return len(xor_out) == 1


def brute_force(w=1):
    A = theta(w)
    Af = flatten(A, w)

    b = 25*w
    res = []
    t = d_aspgen(w)
    res = []
    for length in range(w*5, 1, -1):
        print(length)
        ra = range(0, w*5)
        for p in itertools.combinations(ra, length):
            for l in range(0, w*5):
                if check_perm(Af, w, p, l):
                    print(l, p)
                    res.append((l, p))
                    if len(res) == w*5:
                        return res
    return res

def search_last(w, p, l):
    bp = tuple(map(lambda x: x*2, p))
    print(bp)
    rs = set(range(0, w*5))
    A = theta(w)
    Af = flatten(A, w)
    tested = set()
    for pz in itertools.product('0+', repeat=len(bp)):
        ap = list(bp)
        for i in range(0, len(pz)):
            if pz[i] == '+':
                ap[i] = (ap[i] + 1) % (w*5)
        print(ap)
        rrs = rs.difference(set(ap))
        count = 0
        print(len(rrs))
        for ne in itertools.combinations(rrs, 14 - len(ap)):
            tpm = ap + list(ne)
            if check_perm(Af, w, tpm, l):
                print((l, tpm))
            count += 1

def search_sat(w):
    Ap = theta(w)
    Apf = flatten(Ap, w)

    Cp = []
    Rp = []
    for i in range(0, 5):
        Cp.append([None] * w)
        Rp.append([None] * w)

    for x in range(0, 5):
        for z in range(0, w):
            Cpi = []
            Rpi = None
            for y in range(0, 5):
                Cpi.append((x, y, z))
                if Rpi == None:
                    Rpi = Ap[x][y][z]
                else:
                    Rpi = Rpi.intersection(Ap[x][y][z])
            Cp[x][z] = d_cxor(Apf, Cpi)
            Rp[x][z] = Rpi

    MCp = [None] * (5*w)
    MRp = [None] * (5*w)

    for rx in range(0, 5):
        for rz in range(0, w):
            p = sha3ri(w, rx, rz)
            Cs = ['F'] * (5*w)
            Rs = ['F'] * (5*w)

            for i in sorted(list(set(map(lambda y: sha3i(w, y[0], y[1], y[2]) % (5*w), Rp[rx][rz])))):
                Rs[i] = 'T'

            for i in sorted(list(set(map(lambda y: sha3i(w, y[0], y[1], y[2]) % (5*w), Cp[rx][rz])))):
                Cs[i] = 'T'

            MCp[p] = ''.join(Cs)
            MRp[p] = ''.join(Rs)
            print(rx, rz, rx*w + rz, MRp[p], m_itop(w, Rp[rx][rz]))
            print(rx, rz, rx*w + rz, MCp[p], m_itop(w, Cp[rx][rz]))

    results = {}

    for p in range(0, 5*w):
        tag = "keccak-attacks-theta-inverse-w" + str(w) + "-p" + str(p)

        m = hf.models()
        m.start(tag, recreate=True)
        hf.models.vars.write_header()
        hf.models.vars.write_assign(['cresult'])

        cresult = ['and']
        for j in range(0, len(MRp[p])):
            oc = MRp[p][j]
            xor = ['xor']
            for i in range(0, 5*w):
                var = 'a' + str(i)
                value = MCp[i][j]
                xor.append(('and', var, value))
            xor = tuple(xor)
            cresult.append(('equal', oc, xor))
        cresult = tuple(cresult)
        hf.models.vars.write_clause('cresult', cresult, '01-problem.txt')

        m.collapse()
        m.build()
        m.run(count=1)

        rg = m.load_results_generator()
        for r in rg:
            indices = []
            for i in range(0, 5*w):
                if r['a' + str(i)] == 'T':
                    indices.append(i)
            print(p, len(indices))
            results[p] = list(indices)

    print(results)
    return results



def test_inverse(w):
    for i in range(0, 16):
        s = random_state(w)
        os = ''.join(rtheta(w, s))
        inv_s = ''.join(theta_inverse(w, os))

        #print(s, os, inv_s)
        assert(inv_s == s)
    print("DONE")

w = 64
#search_sat(int(sys.argv[1]))
# test_inverse(w)
# brute_force(w)
#search_last(w, (2, 3, 6, 7, 8, 9, 10, 13, 14, 15), 1)

inv_map_to_bin(8)
