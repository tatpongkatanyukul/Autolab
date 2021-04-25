import subprocess

import misc_tools as mt

def cmd(testcmd, itxt, rtime):

    if len(testcmd.strip()) < 1:
        return True, ''

    runcmd = testcmd
    cmd_chain = runcmd.split(';')

    rout = ''
    run_complete = True

    for i, c in enumerate(cmd_chain):

        tcmd = c.strip()
        print('cmd: run ({}): {}'.format(i, mt.nice_text(tcmd, truncate=True, maxlen=80)))

        ctokens = c.split(' ')
        if len(ctokens[0]) < 1:
            ctokens = ctokens[1:]

        try:
            prc = subprocess.run(ctokens,
                                 input=str.encode(itxt),
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 timeout=rtime)

            rout += str(prc.stdout, 'utf-8')

            if len(prc.stderr) > 0:
                print('cmd: stderr:', prc.stderr)
                run_complete = False
                return run_complete, rout


        except Exception as e:
            print('cmd: run ({}): exception: {}'.format(i, e))
            run_complete = False
            return run_complete, rout

        # end try-except
    # end for
    return run_complete, rout
    

if __name__ == '__main__':
    # r1, r2 = cmd("python readQ_aux1.py student/Q1.txt", "dummyinput", 1)
    # print('r1 = ', r1)
    # print('r2 = ', r2)
    # r1, r2 = cmd("g++ student/P4.cpp -o p.exe; ./p.exe", "dummyinput", 1)
    # print('r1 = ', r1)
    # print('r2 = ', r2)

    # r1, r2 = cmd("python extDynamicGrader1.py", "dummyinput", 5)
    # print('r1 = ', r1)
    # print('r2 = ', r2) 

    # r1, r2 = cmd("python extDynamicGrader2.py", "dummyinput", 5)
    # print('r1 = ', r1)
    # print('r2 = ', r2) 

    r1, r2 = cmd("python extCustomJsonTE1.py ./cfg/ecjte1FE0.cfg 1.0 HidNum", "dummyinput", 5)
    print('r1 = ', r1)
    print('r2 = ', r2)

