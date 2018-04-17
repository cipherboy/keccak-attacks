#!/usr/bin/env python3

import hash_framework as hf

import time, sys, os, random

run = False
release = False
if '--run' in sys.argv:
    run = True
if '--release' in sys.argv:
    release = True
if '-h' in sys.argv or '--help' in sys.argv:
    print(sys.argv[0] + " [--run] [--release] [--args file] [w r e s]")
    print('---')
    print("Generates models for xof testing. Runs if specified, otherwise only creates models.")
    print("--run - runs the resulting CNF file")
    print("--release - deletes the intermediate stages after creation")
    print("--args file - specify a file to load arguments from")
    print("w - sha3 w")
    print("r - sha3 rounds format (str only)")
    print("e - effective margin (128/256/.../512: as if w=1600)")
    print("b - bits to extract")
    sys.exit(0)

def sha3_xof_recreate_args():
    r_args = sys.argv[1:]
    if run:
        r_args = r_args[1:]
    if release:
        r_args = r_args[1:]

    w = int(r_args[0])
    r = int(r_args[1])
    e = int(r_args[2])
    b = int(r_args[3])

    sha3_xof_recreate(w, r, e, b)

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
        b = int(arg[3])

        sha3_xof_recreate(w, r, e, b)

def sha3_xof_recreate(w, r, e, b):
    margin = e*w//64
    s = b // margin
    if s*margin != b:
        s += 1
    s += 1

    algo = hf.algorithms.sha3(w=w, rounds=r)
    tag = "sha3-xof_recreate-w" + str(w) + "-r" + str(r) + '-e' + str(e) + "-s" + str(s)

    initial_prefixes = []
    for i in range(0, s):
        initial_prefixes.append('s' + str(i))

    prefixes = []
    for p in initial_prefixes:
        prefixes.append('h1' + p)
        prefixes.append('h2' + p)

    m = hf.models()
    m.start(tag, recreate=True)
    print(w, r, e, b, margin, s)

    hf.models.vars.write_header()
    hf.models.generate(algo, prefixes, rounds=r, bypass=True)
    hf.models.vars.write_assign(['cdifferent', 'cknown', 'cchain', 'cloop'])

    cdifferent = ['and']
    for j in range(0, 25*w):
        cdifferent.append(('equal', 'h1s0in' + str(j), 'h2s0in' + str(j)))
    cdifferent = ('not', tuple(cdifferent))
    hf.models.vars.write_clause('cdifferent', cdifferent, '10-different.txt')

    if s > 1:
        cchain = ['and']
        for i in range(0, s-1):
            for j in range(0, 25*w):
                cchain.append(('equal', 'h1s' + str(i) + 'out' + str(j), 'h1s' + str(i+1) + 'in' + str(j)))
                cchain.append(('equal', 'h2s' + str(i) + 'out' + str(j), 'h2s' + str(i+1) + 'in' + str(j)))
        cchain = tuple(cchain)
        hf.models.vars.write_clause('cchain', cchain, '15-chain.txt')

    cknown = ['and']
    for i in range(0, s):
        for j in range(0, margin):
            if i*margin + j >= b:
                break
            cknown.append(('equal', 'h1s' + str(i) + 'out' + str(j), 'h2s' + str(i) + 'out' + str(j)))
    cknown = tuple(cknown)
    hf.models.vars.write_clause('cknown', cknown, '20-known.txt')


    cloop = ['and']
    for i in range(0, s):
        for j in range(0, margin):
            if i*margin + j < b:
                continue
            cloop.append(('equal', 'h1s' + str(i) + 'out' + str(j), 'h2s' + str(i) + 'out' + str(j)))
    cloop = ('not', tuple(cloop))
    hf.models.vars.write_clause('cloop', cloop, '25-loop.txt')



    m.collapse()
    m.build()

    if run:
        t1 = time.time()
        res = m.run(count=1)
        t2 = (time.time() - t1)
        print("Run time: " + str(t2))

        for result in m.load_results():
            h1o_s = ""
            for j in range(0, 25*w):
                h1o_s += result['h1s0in' + str(j)]
            print("h1seed: " + str(h1o_s))
            h2o_s = ""
            for j in range(0, 25*w):
                h2o_s += result['h2s0in' + str(j)]
            print("h2seed: " + str(h2o_s))

            for i in range(0, s):
                o_s = ""
                for j in range(0, 25*w):
                    o_s += result['h1s' + str(i) + 'out' + str(j)]
                print("\th1s" + str(i) + ": " + str(o_s) + " -- " + str(o_s == h1o_s) + " -- "  + str(o_s == h2o_s))
                o_s = ""
                for j in range(0, 25*w):
                    o_s += result['h2s' + str(i) + 'out' + str(j)]
                print("\th2s" + str(i) + ": " + str(o_s) + " -- " + str(o_s == h1o_s) + " -- "  + str(o_s == h2o_s))
    if release:
        os.system("rm -rf *.txt *.bc *.concat *.out")
    print("")

if '--args' in sys.argv:
    sha3_xof_recreate_file()
else:
    sha3_xof_recreate_args()
