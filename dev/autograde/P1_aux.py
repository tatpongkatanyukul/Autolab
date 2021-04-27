from P1 import make_dict

def check_dict(d):
    dkeys = list(d.keys())
    dkeys.sort()

    for k in dkeys:
        print(k, d[k], end='; ')

    print()


if __name__ == '__main__':
    atomic_num = make_dict()
    check_dict(atomic_num)

    print(type(atomic_num))