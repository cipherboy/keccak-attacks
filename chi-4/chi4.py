#!/usr/bin/env python3

import hash_framework as hf
import itertools, random

theta = hf.algorithms._sha3.sha3theta
pi = hf.algorithms._sha3.sha3pi
rho = hf.algorithms._sha3.sha3rho
chi = hf.algorithms._sha3.sha3chi


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


# prove_identity_rho64()
# prove_identity_pi24()
# prove_identity_chi4()
prove_identity_theta()
