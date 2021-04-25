"""
Last Major Update: Apr 24th, 2021
* Add checkcode feature into json_grader
"""

import os
from shutil import copy
import time

# For choosing a grading policy
from base_policies import numtol_policy, parline_policy, exact_policy
from policy2021 import numtol_policy2

from cmd_tool import cmd

import platform
from show_cfgdate import get_fdate
from emform_tools import read_form
from misc_tools import pack_message

# For verifying student's identity
import json
from verify_mod import verify, codebookf

# Verification
VERIFY_FNAME = "student/verify.json"
VERIFY_KEY = "checkcode"

def clean_folder(target_folder, confirm=True):
    print('clean_folder: clean', target_folder)

    if confirm:
        c = input('Confirm cleaning [y|n]:')

        if c != 'y':
            print('clean_folder: cancel cleaning.')
            return

    fs = os.listdir(target_folder)
    for f in fs:
        p = os.path.join(target_folder, f)
        os.remove(p)

    print('clean_folder: cleaning is done.')

def get_Grading_Table(directive_fname):
    Grading_Table = []
    f = open(directive_fname, 'r')
    i = 0
    for line in f:

        ## Clean white spaces preceding text
        for j, c in enumerate(line):
            if (c == ' ') or (c == '\t') or (c == '\n'):
                continue
            else:
                line = line[j:]
                break
        # end for j, c

        ## Allow comment out the line
        if line[0] == '#':
            continue

        # It is not a directive
        if '\;' not in line:
            continue

        if i > 0: # skip header
            px, score, student, runtest, runtime, \
            grader, gattrib, report_mode, test_case = line.split('\;')


            clean_tc = test_case
            if clean_tc[-1] == '\n':
                clean_tc = clean_tc[:-1]

            clean_tc = clean_tc.strip()

            d = {'Px':px, 'score': int(score),
                 'student': student.strip(),
                 'runtest': runtest.strip(),
                 'runtime': runtime.strip(),
                 'grader': grader.strip(),
                 'attrib': gattrib.strip(),
                 'report_mode': report_mode.strip(),
                 'test_case': clean_tc.split(',')}

            Grading_Table.append(d)


        i += 1
    f.close()
    return Grading_Table
# end get_Grading_Table

def get_testcase(tc_txt, tcpath):
    if len(tc_txt) < 1:
        return None, None

    tc_input, tc_ans = tc_txt.split(' ')

    # Get input stream (or dummy if program requires none)
    f = open(os.path.join(tcpath, tc_input), 'r')
    input_txt = f.read()
    f.close()

    # Get reference answer
    f = open(os.path.join(tcpath, tc_ans), encoding='utf-8',
             mode='r')
    ref_txt = f.read()
    f.close()

    return input_txt, ref_txt


def prefix_eachline(text, prefix=" "):
    s = ""
    for line in text.split("\n"):
        s += prefix + line + "\n"

    return s


def grading(policy, policy_attrib, test_out, gt_ans,
            full_score, Px, log, mode='Show'):
    """
    For policy = "external",
        expect policy_attrib to have "command-to-run; max-runtime"
    * Then, it will run:
        "command to run" + score + report
        or "command to run" + score + report + submission (if submission length > 0)
        or "command to run" + score + report + submission + ref.ans (if submission length > 0 and ref.ans is not None)
    Note: submission is obtained from (1) run_grader: output of the cfg main run (2) json_grader: read from student's json

    For example,
        run_grader reached through 
            python dispatcher.py "./cfg/eval2021g.cfg" -autolab
        or
            python dispatcher.py "./cfg/eval2021g.cfg" -autolab -verified
        
        * "./cfg/eval2021g.cfg" has, e.g.,

            P107\; 60\; P107.cpp\; \; 0\; external\; python extpolicy4.py ./cfg/ext4P107.cfg; 360\; HidNum\; 
        
            * command to run = "python extpolicy4.py ./cfg/ext4P107.cfg" 
                actually, it runs "python extpolicy4.py ./cfg/ext4P107.cfg 60 HidNum" 
            * max runtime = "360"

        json_grader reached through 
            python dispatcher.py "./cfg/eval2021g.cfg" -autolab  -json
        or
            python dispatcher.py "./cfg/eval2021g.cfg" -autolab  -json -verified
        
        * "./cfg/eval2021g.cfg" has, e.g.,
    
            Q2\; 120\; student.json\; \; 0\; external\; python extDynamicGrader3.py ./cfg/edg3Q2.cfg; 360\; HidNum\; 

            * command to run = "python extDynamicGrader3.py ./cfg/edg3Q2.cfg"
                actually it runs "python extDynamicGrader3.py ./cfg/edg3Q2.cfg 120 HidNum 'student-answers-for-Q2'"
            * max runtime = "360"
    """            

    # Check file in notepad++ with [view] > [show symbol] > [show all characcters]
    # f = open('debug' + Px + 'out.txt', 'w')
    # f.write(test_out)
    #
    # f = open('debug' + Px + 'gt.txt', 'w')
    # f.write(gt_ans)

    # mode = Show: show all details including reference text
    # mode = Silence: show no details

    test_score = 0

    if policy == 'numtol':
        # numerical tolerance
        test_score = numtol_policy(test_out, gt_ans, full_score, mode, policy_attrib)

    elif policy == 'numtol2':
        # numerical tolerance
        test_score = numtol_policy2(test_out, gt_ans, full_score, mode, policy_attrib)

    # elif policy == 'AutoJudge':
    # It is not ready for production!!!
    #
    #     print("Debug: grading: Autojudge:")
    #     print(" * test_out=", test_out)
    #     print(" * gt_ans=", gt_ans)
    #     test_score = Judge.grading(test_out, gt_ans, full_score, mode, float(policy_attrib))

    elif policy == 'parline':
        # partial credit by line
        test_score = parline_policy(test_out, gt_ans, full_score, mode)

    elif policy == 'external':
        # The external policy python script is specified by policy_attrib
        # E.g., policy_attrib = "python extpolicy3.py test.cfg; 5"
        # "test.cfg" could specify test cases or P1ref.cpp or both

        # print("Debug: grading(...):")
        # print(" * test_out({})=".format(len(test_out)), test_out)
        # print(" * ref_ans({})=".format(type(gt_ans)), gt_ans)

        extpolicy, ext_time = policy_attrib.split(";")

        extpolicy_command = extpolicy + \
                            " " + str(full_score) + \
                            " " + mode

        if len(test_out) > 0:
            packed_output = pack_message(test_out)
            extpolicy_command += " " + packed_output
            if gt_ans is not None:
                packed_ref = pack_message(gt_ans)
                extpolicy_command += " " + packed_ref

        # print("Debug 1: grading: \n   ")
        # # print(os.getcwd())
        # print(os.listdir())

        print("grading: resorting to the external policy:")
        print(" * ", end='')
        run_complete, rout = \
            cmd(extpolicy_command, "dummy input", float(ext_time))

        if run_complete:
            print("grading: the external policy is complete.")
            routlines = rout.split('\n')
            last = routlines[-1]
            test_score = float(last)

            if mode != 'Silence':
                print('grading: external details: <begin>')
                #print(rout)
                print(prefix_eachline(rout, prefix="  "))
                print('grading: external details: <end>')
        else:
            print("grading: cannot complete the external policy.")
            print('grading: external details: <begin>')
            #print(rout)
            print(prefix_eachline(rout, prefix="  "))
            print('grading: external details: <end>')

    else: # exact match (no partial credit/minimal flexibility)
        print("grading: on exact policy")
        test_score = exact_policy(test_out, gt_ans, full_score, mode)

    return test_score


def run_grader(directive, paths, codeverify=False):

    global VERIFY_FNAME, VERIFY_KEY

    if codeverify:
        print("run_grader: verifying student's code ...")
        try:
            # Get student's email
            with open(paths['student_email_json'],
                    encoding='utf-8', mode='r') as f:
                user_json = f.read()

            d = json.loads(user_json)
            print('run_grader: identity =', d['user'])

            # # Get student's code
            with open(VERIFY_FNAME, mode='r') as f:
                verify_txt = f.read()
            verify_dict = json.loads(verify_txt)

            # Verify student's code against verify function
            if not verify(d['user'], verify_dict[VERIFY_KEY], codebookf):
                print('run_grader: verification failed!')
                print('run_grader: verification code does not match!')
                exit(0)

            print('run_grader:', d['user'], 'is verified.')

        except Exception as e:
            print('run_grader: personal code verification: exception:', e)
            print('run_grader: personal code cannot be verified.')
            exit(0)

    #end if VERIFIED


    plat = platform.system()
    print('run_grader: ==================================================')
    print('run_grader:   Run on platform:', plat)
    print('run_grader:   with settings:', directive)
    d = get_fdate(directive)
    print('run_grader:        (last mod. ', d, ')', sep='')
    print('run_grader: ==================================================')


    student_path = paths['student']
    answer_path = paths['answer']
    working_path = paths['working']
    log_file = paths['log_file']

    # Clear log_file
    with open(log_file, 'w') as f:
        f.write('')

    # Create Grading Table: get grading details from directive file
    Grading_Table = get_Grading_Table(directive)

    #print(Grading_Table)
    print('run_grader: total grading', len(Grading_Table), 'problems')

    graded = {}
    for P in Grading_Table:
        print('\nrun_grader: on', P['Px'])
        student_submission = os.path.join(student_path, P['student'])
        if os.path.exists(student_submission):
            print('run_grader: * %s is submitted'%P['student'])
            print('run_grader: * tested with "%s" using %s policy (attributes: %s)' % (P['runtest'],
                                                        P['grader'], P['attrib']))
            print('run_grader: * test case(s):', P['test_case'])

            # Copy student_submission to current working directory
            copy(student_submission, working_path)

            point = 0
            tc_score = P['score'] / len(P['test_case'])

            for i, tc in enumerate(P['test_case']):

                istream, ref_ans = get_testcase(tc.strip(), answer_path)

                begintime_runtest = time.time()
                # Run the test
                run_complete, rout = \
                    cmd(P['runtest'],
                        istream, float(P['runtime']))
                endtime_runtest = time.time()
                print('run_grader: @ Time to run test: {:.2f} s.'.format(endtime_runtest - begintime_runtest))

                # Grade result if run_complete
                if run_complete:

                    #======================================
                    # Grade the output against the answer
                    #======================================

                    begintime_grading = time.time()
                    grading_out = grading(P['grader'], P['attrib'],
                                    rout, ref_ans, tc_score,
                                    P['Px'], log_file,
                                    mode=P['report_mode'])
                    endtime_grading = time.time()
                    print('run_grader: @ Time to grade: {:.2f} s.'.format(endtime_grading - begintime_grading))

                    print('run_grader: * grading ', grading_out)
                    point += grading_out

            graded_point = round(point)
            graded[P['Px']] = graded_point

            # Clean up/Remove student file
            print('run_grader: * Done: clean up {}'.format(P['student']))
            print('run grader: * {} score = {}'.format(P['Px'], graded_point))
            try:
                os.remove(P['student'])
            except Exception as e:
                print('run_grader: ** clean up fails: ', e)

        else:
            print('run_grader: * %s is NOT submitted' % P['student'])
            graded[P['Px']] = 0
    # end for P in Grading_Table
    print() # have a blank line after finishing all gradings.

    # Last line of printing must be score report
    # print(graded)

    csep = ''
    score_txt = '{"scores": {'
    sboard_txt = ''
    total_score = 0
    for P in Grading_Table:
        score_txt += csep + '"%s": %d'%(P['Px'], graded[P['Px']])
        sboard_txt += csep + '%d'%graded[P['Px']]
        total_score += graded[P['Px']]
        if csep == '':
            csep = ', '

    score_txt += '},"scoreboard":[%s, %d]}'%(sboard_txt, total_score)

    if os.path.exists(log_file):
        f = open(log_file, encoding='utf-8', mode='r')
        m = f.read()
        f.close()
        if len(m) > 0:
            print('run_grader: log file content'%P['grader'])
            print(m)
            print("\n\n")

    return score_txt
#end run_grader

def json_grader(submission_json, grading_cfg, gpaths, codeverify=False):
    '''
    json_grader should work similar to run_grader,
    but instead of run the test command afresh through general approach of using subprocess.
    It should:
        (1) read json and get the dict student_all;
        (2) go over Q's from cfg on student_all[Q];
        and (3) evaluate student_all[Q] against ref.
    '''
    plat = platform.system()
    print('json_grader: ==================================================')
    print('json_grader:   Run on platform:', plat)
    print('json_grader:   with settings:', grading_cfg)
    d = get_fdate(grading_cfg)
    print('json_grader:        (last mod. ', d, ')', sep='')
    print('json_grader: ==================================================')

    try:
        student_all = read_form(submission_json)

    except Exception as e:
        print("json_grader: student\'s answers (json) load error:", e)
        return 0
    # end try-except

    global VERIFY_FNAME, VERIFY_KEY

    if codeverify:
        print("json_grader: verifying student's code ...")
        try:
            # Get student's email
            with open(gpaths['student_email_json'],
                    encoding='utf-8', mode='r') as f:
                user_json = f.read()

            d = json.loads(user_json)
            print('json_grader: identity =', d['user'])

            # # Get student's code
            studentcode = student_all[VERIFY_KEY]

            # Verify student's code against the verify function
            if not verify(d['user'], studentcode, codebookf):
                print('json_grader: verification failed!')
                print('json_grader: verification code does not match!')
                exit(0)

            print('json_grader:', d['user'], 'is verified.')

        except Exception as e:
            print('json_grader: personal code verification: exception:', e)
            print('json_grader: personal code cannot be verified.')
            exit(0)

    #end if VERIFIED

    answer_path = gpaths['answer']
    working_path = gpaths['working']

    # Create Grading Table: get grading details from directive file
    Grading_Table = get_Grading_Table(grading_cfg)

    #print(Grading_Table)
    print('json_grader: total grading', len(Grading_Table), 'problems')


    graded = {}
    for P in Grading_Table:
        if submission_json != os.path.join(gpaths['student'], P['student']):
            print("\njson_grader: submission file '{}' does not match the configuration {}.".format(submission_json, P['student']) )
            print(" * Consult the author's autograder to resolve the problem (check eval. cfg).")
            exit(0)


        print('\njson_grader: on question', P['Px'])
        student_submission = student_all[P['Px']]


        _, ref_ans = get_testcase(P['test_case'][0].strip(), answer_path)

        # print("Debug 2: json_grader: student_submission:")
        # print("* ", student_submission)



        grading_out = grading(P['grader'], P['attrib'],
                        student_submission, ref_ans, P['score'],
                                    P['Px'], gpaths['log_file'],
                                    mode=P['report_mode'])

        graded[P['Px']] = round(grading_out)
        print('json grader: * {} score = {}'.format(P['Px'], graded[P['Px']]))

    # end for P in Grading_Table
    print() # have a blank line after finishing all gradings.

    # Last line of printing must be score report
    # print(graded)

    csep = ''
    score_txt = '{"scores": {'
    sboard_txt = ''
    total_score = 0
    for P in Grading_Table:
        score_txt += csep + '"%s": %d'%(P['Px'], graded[P['Px']])
        sboard_txt += csep + '%d'%graded[P['Px']]
        total_score += graded[P['Px']]
        if csep == '':
            csep = ', '

    score_txt += '},"scoreboard":[%s, %d]}'%(sboard_txt, total_score)

    return score_txt
# end json_grader

def test_run_grader():
    directive = "./cfg/ans2021f.cfg"
    grader_paths = {'student': './student',
             'answer': './answers',
             'working': '.',
             'log_file': './glog.txt',
             'student_email_json': './settings.json',
             'student_vfile': './student/verify.txt'}


    scores = run_grader(directive, grader_paths)
    print('runtest_tool: main: ', scores)

def test_json_grader():

    grader_paths = {'student': './student',
             'answer': './answers',
             'working': '.',
             'log_file': './glog.txt',
             'student_email_json': './settings.json',
             'student_vfile': './student/verify.txt'}

    student_submission = os.path.join(grader_paths['student'],
                                      "student.ans")

    s = json_grader(student_submission, "./cfg/eval_win_json_grader.cfg",
                grader_paths)
    print('runtest_tool: test json_grader s = ', s)

if __name__ == '__main__':
    test_json_grader()