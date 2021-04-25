"""
This is to show ans.cfg date.
The rationale is that:
windows and unix will use different cfg, e.g.,
cfg/ans.cfg for running/testing
* wincfg/ans.cfg saves a windows version
* unixcfg/ans.cfg saves a unix version
I am afraid that I may forget to do the changing.
So seeing a timestamp may give me some clue if I have used the latest one.
"""

import pathlib
import datetime

def get_fdate(targetf):
    fname = pathlib.Path(targetf)
    assert fname.exists(), 'No such file: {}'.format(fname)

    ctime = datetime.datetime.fromtimestamp(fname.stat().st_mtime)
    return ctime


if __name__ == '__main__':
    target = './cfg/ans.cfg'
    s = get_fdate(target)
    print(type(s))
    print(str(s))
    print(s)