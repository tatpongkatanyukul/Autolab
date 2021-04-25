"""
Last Major Update: Feb 3rd, 2021

Pilot policy for flexible external policy.
The idea is to have a general flexible policy
capable of multiple modes of assessment.
This one is just to compile and run C++ program.

But the possibilities are enormous.
For example:
* C/C++ compilation and run
    {"student": 'P3.cpp', "config": 'testcases.cfg'}
    --> g++ P3.cpp -o P3.exe
            or (for build and link) g++ -c -g P8.cpp -o P8.o; g++ -c -g P8_auxT.cpp -o P8_aux.o; g++ -o P8.exe P8.o P8_aux.o
    --> run P3.exe on each test case and compare against ref text.
Note: I may extend this to a dedicated mode "prefix/suffix parline" for efficiency
* Run against reference program (### LATER ###)
    {"student": 'P4.cpp', "config": 'ref_testcases_tol.cfg'}
"""

import sys
import json
from cmd_tool import cmd
from policy2021 import numtol_policy2
import time

def buildandrun(policy_par):

    student_score = 0

    # Read configuration file
    with open(policy_par['config'], 'r') as f:
        cfg_txt = f.read()
        cfg = json.loads(cfg_txt)


    # Default values
    default_val = {"pre-run time": 120, "runtime": 5, "post-run time": 60,
                   "pre-run": '',
                   "run": '',
                   "post-run": '',
                   "numtol": 0.05,
                   "testcases": None, "ref prog": None}
    for k in default_val:
        if k in cfg:
            continue

        cfg[k] = default_val[k]
    # End for default_val

    # Debug
    # cfg_test = json.dumps(cfg)
    # with open("extpolicy1_debug.txt", 'a') as f:
    #     f.write(cfg_test)

    # Pre-run
    istream = "dummy input"
    prerun_command = cfg["pre-run"]

    begin_prerun = time.time()
    run_complete, rout = \
        cmd(prerun_command,
            istream, cfg['pre-run time'])
    end_prerun = time.time()
    print(policy_par['policy'] + ":",
          '@ Time spent in pre-run: {:.2f} s.'.format(end_prerun - begin_prerun))

    if run_complete:
        print(policy_par['policy'] + ":", "pre-run is complete.")
    else:
        print(policy_par['policy'] + ":", "pre-run error=", rout)
        return 0

    #======
    # Run
    #======

    # Go through each test cases
    tc_score = float(policy_par['score']) / len(cfg["testcases"]) # score for each test case if get it right

    begin_run = time.time()
    for i, case in enumerate(cfg["testcases"]):
        print(policy_par['policy'] + ":", 'case ({}) {}'.format(i, case))

        #####################
        # Run the test case
        #####################

        # Get input stream (or dummy if program requires none)
        with open(case[0], 'r') as f:
            istream = f.read()

        run_complete, studentout = \
            cmd(cfg["run"], istream, float(cfg['runtime']))

        # Grade result if run_complete
        if run_complete:
            # Compare student's output against the ref text

            # Get the reference answer
            with open(case[1], encoding='utf-8', mode='r') as f:
                ref_ans = f.read()

            # Grade the output based on reference
            s = numtol_policy2(studentout, ref_ans,
                          tc_score, policy_par["mode"], cfg["numtol"], neg_handling=False)
            student_score += s
        else:
            print(policy_par['policy'] + ":", 'case ({})'.format(i),
                  ': error=', studentout)
    # end for i, case
    end_run = time.time()
    print(policy_par['policy'] + ":",
          '@ Time spent in (main/test) run: {:.2f} s.'.format(end_run - begin_run))


    # Finish testing. Run the post-run
    # os.remove(run_filename)
    istream = "dummy input"

    begin_postrun = time.time()
    run_complete, rout = \
        cmd(cfg["post-run"], istream, cfg['post-run time'])
    end_postrun = time.time()
    print(policy_par['policy'] + ":",
          '@ Time spent in post-run: {:.2f} s.'.format(end_postrun - begin_postrun))


    if run_complete:
        print(policy_par['policy'] + ":", "post-run is complete.")

    else:
        print(policy_par['policy'] + ":", "post-run error=", rout)


    return student_score


def main_debug():
#if __name__ == '__main__':
    ## Debug
    test_param = {"policy": "this",
                  "config": "./cfg/ext2P6.cfg",
                  "score": 10,
                  "mode": "Show"}
    score = buildandrun(test_param)
    print(score, end='')

if __name__ == '__main__':
#def tmp():
    var_list = ["policy",   # this policy
                "config",   # configuration file
                "score",    # full score
                "mode"]     # report mode: "Show"/"Silence"

    # =========
    # Debugging
    # =========
    # msg = ''
    # for i in range(len(sys.argv)):
    #     msg += sys.argv[i] + "\n"
    #
    # with open("extpolicy1_debug.txt", 'w') as f:
    #     f.write(msg)

    msg = ''
    test_param = {}
    for i, arg in enumerate(sys.argv):
        test_param[var_list[i]] = arg

    msg += str(test_param)
    with open("extpolicy2_debug.txt", 'w') as f:
        f.write(msg)

    score = buildandrun(test_param)

    print(score, end='')

