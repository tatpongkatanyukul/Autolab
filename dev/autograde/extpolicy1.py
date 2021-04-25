"""
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
from base_policies import numtol_policy, parline_policy
import os

def buildandrun(policy_par):

    student_score = 0

    # Read configuration file
    with open(policy_par['config'], 'r') as f:
        cfg_txt = f.read()
        cfg = json.loads(cfg_txt)


    # Default values
    default_val = {"buildtime": 120, "runtime": 5, "testcases": None, "ref prog": None}
    for k in default_val:
        if k in cfg:
            continue

        cfg[k] = default_val[k]
    # End for default_val

    # Debug
    # cfg_test = json.dumps(cfg)
    # with open("extpolicy1_debug.txt", 'a') as f:
    #     f.write(cfg_test)

    run_filename = 'student.exe'
    # Compile C++
    istream = "dummy input"

    build_command = "g++ " + \
                    policy_par["student"] + " -o " + run_filename

    run_complete, rout = \
        cmd(build_command,
            istream, cfg['buildtime'])

    if run_complete:
        print("extpolicy1: compilation is complete.")

        # uncomment to credit a compilable program. But, nah! Feb 3, 2021.
        # student_score += 1

    else:
        print("extpolicy1: error =", rout)
        return 0
        # Debug
        # with open("extpolicy1_debug.txt", 'a') as f:
        #     f.write("\nrun_complete = " + str(run_complete))
        #     f.write("\nrout = " + rout)
        #     f.write("\nstudent_score = " + str(student_score))

    # Go through each test cases
    tc_score = float(policy_par['score']) / len(cfg["testcases"]) # score for each test case if get it right

    for i, case in enumerate(cfg["testcases"]):
        print('extpolicy1: test case', i, case)

        #####################
        # Run the test case
        #####################


        # Get input stream (or dummy if program requires none)
        with open(case[0], 'r') as f:
            istream = f.read()

        run_complete, studentout = \
            cmd(run_filename, istream, float(cfg['runtime']))

        # Grade result if run_complete
        if run_complete:
            # Compare student's output against the ref text

            # Get the reference answer
            with open(case[1], encoding='utf-8', mode='r') as f:
                ref_ans = f.read()

            # Grade the output based on reference
            s = numtol_policy(studentout, ref_ans,
                          tc_score, policy_par["mode"], "0.05")
            student_score += s
    # end for i, case

    # Finish testing. Clean up the file
    os.remove(run_filename)

    return student_score


def main_debug():
    ## Debug
    test_param = {"policy": "this", "student":  "P3.cpp",
                  "config": "./answers/testP3.cfg", "score": 10,
                  "problem": "P3", "log": "log.txt", "mode": "Show"}
    score = buildandrun(test_param)
    print(score, end='')

if __name__ == '__main__':
    var_list = ["policy",   # this policy
                "student",  # student submission
                "config",   # configuration file
                "score",    # full score
                "problem",  # problem id
                "log",      # log file
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
    with open("extpolicy1_debug.txt", 'w') as f:
        f.write(msg)

    score = buildandrun(test_param)

    print(score, end='')

