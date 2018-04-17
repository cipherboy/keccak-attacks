#!/usr/bin/env python3

import hash_framework as hf

import time, sys, os, random, json, itertools

run = True
release = False
if '--release' in sys.argv:
    release = True
if '-h' in sys.argv or '--help' in sys.argv:
    print(sys.argv[0] + " [--release] [--args file] [w r e]")
    print('---')
    print("Generates models for xof testing. Runs if specified, otherwise only creates models.")
    print("--release - deletes the intermediate stages after creation")
    print("--args file - specify a file to load arguments from")
    print("w - sha3 w")
    print("r - sha3 rounds format (str only)")
    print("e - effective margin (128/256/.../512: as if w=1600)")
    sys.exit(0)

def sha3_xof_recreate_args():
    r_args = sys.argv[1:]
    if release:
        r_args = r_args[1:]

    w = int(r_args[0])
    r = int(r_args[1])
    e = int(r_args[2])

    sha3_xof_recreate(w, r, e)

def sha3_xof_recreate_file():
    fname = sys.argv[-1]
    args = open(fname, 'r').read().split('\n')
    for s_arg in args:
        if len(s_arg) == 0:
            continue
        arg = s_arg.split(" ")
        w = int(arg[0])
        r = int(arg[1])
        e = int(arg[2])

        sha3_xof_recreate(w, r, e)

def sha3_xof_recreate(w, r, e):
    margin = e*w//64

    algo = hf.algorithms.sha3(w=w, rounds=r)
    tag = "sha3-xof_tree-w" + str(w) + "-r" + str(r) + '-e' + str(e)

    r_tree = {}

    for elm in itertools.product('TF', repeat=4*margin):
        m = hf.models()
        m.start(tag, recreate=True)

        hf.models.vars.write_header()
        hf.models.generate(algo, ['h1', 'h2', 'h3'], rounds=r, bypass=True)
        hf.models.vars.write_assign(['cassign', 'cchain'])

        cassign = ['and']
        for j in range(0, margin):
            cassign.append(('equal', 'h1in' + str(j), elm[j]))
        for j in range(0, margin):
            cassign.append(('equal', 'h1out' + str(j), elm[j+margin]))
        for j in range(0, margin):
            cassign.append(('equal', 'h2out' + str(j), elm[j+2*margin]))
        for j in range(0, margin):
            cassign.append(('equal', 'h3out' + str(j), elm[j+3*margin]))
        cassign = tuple(cassign)
        hf.models.vars.write_clause('cassign', cassign, '10-assign.txt')

        cchain = ['and']
        for j in range(0, 25*w):
            cchain.append(('equal', 'h1out' + str(j), 'h2in' + str(j)))
            cchain.append(('equal', 'h2out' + str(j), 'h3in' + str(j)))
        cchain = tuple(cchain)
        hf.models.vars.write_clause('cchain', cchain, '15-chain.txt')

        m.collapse()
        m.build()

        t1 = time.time()
        res = m.run(count=1)
        t2 = (time.time() - t1)
        print("Run time: " + str(t2))

        if res:
            result = m.load_results()[0]
            for j in range(0, margin):
                assert(result['h1in' + str(j)] == elm[j])
            for j in range(0, margin):
                assert(result['h1out' + str(j)] == elm[j+margin])
            for j in range(0, margin):
                assert(result['h2out' + str(j)] == elm[j+2*margin])
            for j in range(0, margin):
                assert(result['h3out' + str(j)] == elm[j+3*margin])
            el = len(elm)
            pre = ''.join(elm[:margin])
            preleaf = ''.join(elm[margin:2*margin])
            postleaf = ''.join(elm[2*margin:3*margin])
            leaf = ''.join(elm[2*margin:])
            if not pre in r_tree:
                r_tree[pre] = {}
            if not preleaf in r_tree[pre]:
                r_tree[pre][preleaf] = {}
            if not postleaf in r_tree[pre][preleaf]:
                r_tree[pre][preleaf][postleaf] = []
            r_tree[pre][preleaf][postleaf].append(leaf)
            print(r_tree)
            #r_tree[pre][preleaf].append(leaf)


    f = open('/tmp/xof-tree-w' +str(w) + '-r' + str(w) + '.json', 'w')
    json.dump(r_tree, f)

if '--args' in sys.argv:
    sha3_xof_recreate_file()
else:
    sha3_xof_recreate_args()
