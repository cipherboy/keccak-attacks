
import random, itertools
from functools import partial

def sha3i(w, x, y, z):
    return w*(5*y + x) + z

def sha3r(w, p):
    z = p % w
    r = p // w
    x = r % 5
    r = r // 5
    y = r
    return (x, y, z)


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

def d_add(s, p):
    print(s, p)
    x, y, z = list(s)[0]
    loc = sha3i(w, x, y, z)
    return loc


def brute_force(w=1):
    A = theta(w)
    f = flatten(A, w)
    b = 25*w
    xors = {}
    inverse = []

    for l in range(1, b):
        ro = list(range(b))
        random.shuffle(ro)
        for p in ro:
            lp = [p]
            sp = set(lp)
            for ep in set(xors):
                sep = set(ep)
                np = tuple(sep ^ sp)
                if len(np) > 0  and np not in xors:
                    ns = d_xor(f, np)
                    xors[np] = ns
                    if len(ns) == 1:
                        print((ns, np))

            if not tuple(lp) in xors:
                xors[tuple(lp)] = f[p]
            print(len(xors))

    return inverse


def a(w, x, y, z, sz1, sz2, sx1, sx2, ox, oy, oz):
    xp = (x + sx1) % 5
    xpp = (x + sx2) % 5

    cp = [((x + ox) % 5, (y + oy) % 5, (z + oz) % w)]
    for ny in range(0, 5):
        cp.append((xp % 5, ny, (z + sz1) % w))
        cp.append((xpp % 5, ny, (z + sz2) % w))

    if not len(set(cp)) == 11:
        return False

    p = list(map(lambda a: sha3i(w, a[0], a[1], a[2]), cp))

    r = d_xor(f, p)
    # if not (len(r) == 1 or list(r)[0] == (x, y, z)):
    #     print((w, (x, y, z), len(r), sorted(cp), sorted(p)))

    return len(r) == 1 and list(r)[0] == (x, y, z)


def test():
    c1 = 0
    c2 = 0

    for w in [1, 2, 4, 8, 16, 32, 64]:
        A = theta(w)
        f = flatten(A, w)

        sc2 = c2

        for sx1 in range(0, 5):
            for sx2 in range(0, 5):
                for sz in range(0, w):
                    for sz2 in range(0, w):
                        for ox in range(0, 5):
                            for oy in range(0, 5):
                                for oz in range(0, w):
                                    def na(w, x, y, z):
                                        return a(w, x, y, z, sz, sz2, sx1, sx2, ox, oy, oz)

                                    c1 += 1
                                    if check(na, w):
                                        c2 += 1
                                        print((w, sz, sz2, sx1, sx2, ox, oy, oz))

        print((w, c1, c2, sc2))
        if c2 == sc2:
            break

res = brute_force(w=1)
