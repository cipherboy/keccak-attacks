import hash_framework as hf

def fp(w, rounds):
    algo = hf.algorithms.sha3(w=w, rounds=rounds)
    tag = "keccak-attacks-fixed-point"

    m = hf.models()
    m.start(tag, recreate=True)
    hf.models.vars.write_header()
    hf.models.generate(algo, ['h1'], rounds=rounds, bypass=True)
    hf.models.vars.write_assign(['cfixed'])

    cfixed = ['and']
    for i in range(0, 25*w):
        cfixed.append(('equal', 'h1in' + str(i), 'h1out' + str(i)))
    cfixed = tuple(cfixed)
    hf.models.vars.write_clause('cfixed', cfixed, '50-fixed.txt')

    m.collapse()
    m.build()
    m.run(count=1000)

    rg = m.results_generator(algo, prefixes=["h1"])
    for r in rg:
        print(r['h1in'], r['h1out'])


def block_extender(w, rounds, margin):
    algo = hf.algorithms.sha3(w=w, rounds=rounds)
    tag = "keccak-attacks-fixed-point"

    m = hf.models()
    m.start(tag, recreate=True)
    hf.models.vars.write_header()
    hf.models.generate(algo, ['h1'], rounds=rounds, bypass=True)
    hf.models.vars.write_assign(['cfixed', 'cinput'])

    cinput = ['and']
    for i in range(margin, 25*w):
        cinput.append(('equal', 'h1in' + str(i), 'F'))
    cinput = tuple(cinput)
    hf.models.vars.write_clause('cinput', cinput, '50-input.txt')

    cfixed = ['and']
    for i in range(margin, 25*w):
        cfixed.append(('equal', 'h1in' + str(i), 'h1out' + str(i)))
    cfixed = tuple(cfixed)
    hf.models.vars.write_clause('cfixed', cfixed, '50-fixed.txt')

    m.collapse()
    m.build()
    m.run(count=10000000)

    rg = m.results_generator(algo, prefixes=["h1"])
    count = 0
    for r in rg:
        # print(r['h1in'], r['h1out'])
        count += 1
    print(count)


def test_fp(w, rounds, s):
    algo = hf.algorithms.sha3(w=w, rounds=rounds)
    oet = hf.algorithms._sha3.perform_sha3({}, s, None, rounds=rounds, w=w)
    et = algo.sanitize(oet)
    print(et['in'], et['out'])

block_extender(2, 1, 34)
#block_extender(1, 2, 17)
# fp(1, 3)

# test_fp(1, 3, "FFFFFFFFTFFTTFTFFTFFFFFFT")
