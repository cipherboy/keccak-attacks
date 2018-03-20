#!/usr/bin/env python3

import hash_framework as hf
import itertools

chi = hf.algorithms._sha3.sha3chi

w = 1
s = ['i' + str(i) for i in range(0, 25*w)]
# o = chi(w, chi(w, chi(w, chi(w, s))))
o = chi(w, chi(w, chi(w, chi(w, s))))

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
o0 = flatten(o[0])
print()
for pos in range(0, len(s)):
    for etvs in itertools.product('TF', repeat=5):
        e_vars = sorted(list(hf.boolean.var_find(o[pos])))
        et = {}
        for i in range(0, len(e_vars)):
            et[e_vars[i]] = etvs[i]
        ov = hf.boolean.var_eval(o[pos], et)
        assert(ov == et['i' + str(pos)])
