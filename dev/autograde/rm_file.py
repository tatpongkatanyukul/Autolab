import os
import sys

if __name__ == '__main__':
    target_file = sys.argv[1]
    # f = open("debug.txt", 'w')
    # f.write("target="+target_file)
    # f.close()
    os.remove(target_file)
