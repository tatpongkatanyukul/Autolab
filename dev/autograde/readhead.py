"""
Read header of the c++ file
"""

import sys
import re

def readhead(fname):

    print('readhead:', fname)
    f = open(fname, 'r')

    content = f.read()
    # content = "No multiline comment"
    # content = "With /* multiline */ comment"
    # content = "With /* multi\nline */ comment"

    r = re.search("/\*.*\*/", content, re.DOTALL)
    if r:
        b, e = r.span(0)
        return content[b:e]

    return None




if __name__ == '__main__':

    fname = 'P5.cpp'
    if len(sys.argv) > 1:
        fname = sys.argv[1]

    # h = readhead(fname)
    # print(h)

    c = "aloha /* test */ bye"
    # r = re.search("/\*.*\*/", c)
    # print(r)
    # b, e = r.span(0)
    # print(c[b:e])

    print(readhead('P4.cpp'))

