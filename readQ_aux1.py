"""
Read a text file and print out
"""

import sys

if __name__ == '__main__':

    fname = 'Q1.txt'
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    else:
        print('readQ_aux1: no filename (', filename, ') specified.')
        exit(1)

    f = open(fname, 'r')

    content = f.read()
    print(content)


