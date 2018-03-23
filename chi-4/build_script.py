def gen_specs():
    import itertools
    iota = set()
    niota = set()
    for length in range(5, 6):
        for func in itertools.product('trpci', repeat=length):
            func = ''.join(func)
            if 'i' in func:
                skip = False
                for i in range(0, len(func) - 1):
                    if func[i] == func[i+1]:
                        skip = True
                    if not 't' in func or not 'c' in func:
                        skip = True
                if not skip:
                    iota.add(func)
            else:
                skip = False
                for i in range(0, len(func) - 1):
                    if func[i] == func[i+1]:
                        skip = True
                if not skip:
                    niota.add(func)
    print(len(iota), len(niota))

    s = ""
    for spec in iota:
        s += spec + " "

    print("for spec in " + s + "; do")
    print("\tfor r in `seq 1 24`; do")
    print("\t\t./cycles $r $spec > order-w1-r$r-f$spec.txt &")
    print("\tdone")
    print("\twait")
    print("done")
    print("\n\n\n")

    s = ""
    for spec in niota:
        s += spec + " "

    print("for spec in " + s + "; do")
    print("\t./cycles 1 $spec > order-w1-r1-f$spec.txt &")
    print("done")
    print("wait")

gen_specs()
