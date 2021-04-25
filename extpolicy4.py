"""
Last Major Update: Apr 17th, 2021
(Adapted from extpolicy3.py)

Keys
* to accommodate additional attributes: student_output and ref
    Note: the additional attributes are only available when len(student_output) > 0

Call
    python extpolicy4.py ./cfg/ext4P108.cfg
    python extpolicy4.py ./cfg/ext4P108.cfg 60 HidNum
    python extpolicy4.py ./cfg/ext4P108.cfg 60 HidNum "myoutput\nline2" "myref\nline2"
"""

import sys
import json
from cmd_tool import cmd
from policy2021 import numtol_policy2
import time

from runtest_tool import prefix_eachline

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
                   "pre-run-output": "show", "main-run-output": "noshow",
                   "post-run-output": "show",
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

        if cfg["pre-run-output"] == "show":
            print("pre-run details:")
            print(prefix_eachline(rout, prefix="  "))

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

        if cfg["post-run-output"] == "show":
            print("post-run details:")
            print(prefix_eachline(rout, prefix="  "))


    else:
        print(policy_par['policy'] + ":", "post-run error=", rout)

    return student_score

if __name__ == '__main__':

    # Default
    params = {"policy": "extpolicy4.py",
                "config": "./cfg/ext4P108.cfg",
                "score": 60,
                "mode": "Show",
                "mainrun_output": "", # empty text, if cfg run =" "
                "mainref": None}  # None type,  if cfg run =" "

    var_list = ["policy",   # this policy
                "config",   # configuration file
                "score",    # full score
                "mode",     # report mode, e.g., "Show"/"Silence"/"HidNum"
                "mainrun_output", # output captured from the main run session, aka student_output
                "mainref"]    # reference output

    for i, arg in enumerate(sys.argv):
        params[var_list[i]] = arg

    # print("Debug: extpolicy4 main: params=", params)

    score = buildandrun(params)

    print(score, end='')

