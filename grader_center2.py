"""
Predecessor: mm_grader_center.py
Created: Dec 26th, 2020.
For:
(1) accommodating C++ (compilation and run)
(2) refactoring code
(3) allowing easier debugging

==================================================
Take over control from driver.sh
Assuming
1. student's submission: current directory/student (see paths if change)
    It copies only "target" files to its working directory to grade.
    (This is to safeguard against accident write over grader files.)
    The "target" files are specified in the directive file, e.g., ans.txt.
2. sys.argv[1]: a directive file indicating:
Problem #: Points; Student Submission File; Run File; Test Case in, ans;
3. Three MODES: Autolab (main), Test (single test on PC),
    Local Batch (back up when Autolab server gets stuck).
    Local Batch takes tar files.
4. Identity verification option
    (through secret code defined in secret function)
    4.1 Run gen_emailcode('email file', 'output_email_code_file')
        to get the email-code pairs.
        See D:\Classes\00FCP\2019b\L00a\local_autograde\sandbox1 for example.
        E.g., gen_emailcode('email_list.txt', 'emailcode.txt')
    4.2 Hand codes to students.
    4.3 Ask students to put code in code file, e.g., code.txt.
    4.4 Include code.txt in the tar file
"""

from shutil import copy
import os
import sys
import subprocess
import tarfile
import json

from verify_mod import verify, codebookf, read_student_verf

def clean_folder(target_folder, confirm=True):
    print('Clean folder:', target_folder)

    if confirm:
        c = input('Confirm cleaning [y|n]:')

        if c != 'y':
            print('Cancel cleaning.')
            return

    fs = os.listdir(target_folder)
    for f in fs:
        p = os.path.join(target_folder, f)
        os.remove(p)

    print('cleaning is done.')


def run_grader(directive, runtest_command, runtest_suffix,
               grader_command, paths):

    student_path = paths['student']
    answer_path = paths['answer']
    working_path = paths['working']
    log_file = paths['log_file']

    # Clear log_file
    with open(log_file, 'w') as f:
        f.write('')

    # Create Grading Table: get grading details from directive file
    Grading_Table = []
    f = open(directive, 'r')
    i = 0
    for line in f:
        if i > 0:
            px, score, student, runtest, grader, test_case = line.split(';')

            clean_tc = test_case
            if clean_tc[-1] == '\n':
                clean_tc = clean_tc[:-1]

            clean_tc = clean_tc.strip()

            d = {'Px':px, 'score': int(score),
                 'student': student.strip(),
                 'runtest': runtest.strip(),
                 'grader': grader.strip(),
                 'test_case': clean_tc.split(',')}

            ## Allow comment out the line
            if px[0] != '#':
                Grading_Table.append(d)

        i += 1
    f.close()

    #print(Grading_Table)
    print('GC: total grading', len(Grading_Table), 'problems')

    graded = {}
    for P in Grading_Table:
        print('GC: on', P['Px'])
        student_submission = os.path.join(student_path, P['student'])
        if os.path.exists(student_submission):
            print('GC: * %s is submitted'%P['student'])
            print('GC: * tested with %s using %s' % (P['runtest'], P['grader']))
            print('GC: * test case(s):', P['test_case'])

            # Copy student_submission to current working directory
            copy(student_submission, working_path)

            point = 0
            num_tc = len(P['test_case'])

            for tc in P['test_case']:

                tc_input, tc_ans = tc.strip().split(' ')
                # print(tc_input)
                # print(tc_ans)

                # Get input stream (or dummy if program requires none)
                f = open(os.path.join(answer_path,tc_input), 'r')
                istream = f.read()
                f.close()

                # Get correct answer
                f = open(os.path.join(answer_path,tc_ans), encoding='utf-8',
                         mode='r')
                ans = f.read()
                f.close()

                # Run test
                rout = ''
                run_complete = False

                # print("P['test']=", P['test'])

                # Compile and run

                try:
                    prc = subprocess.run([runtest_command, P['runtest'],
                                          runtest_suffix],
                                         input=str.encode(istream),
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE,
                                         timeout=1)

                    rout = str(prc.stdout, 'utf-8')
                    run_complete = True

                    print('# DEBUG: rout = ', rout)
                    print('# DEBUG: ans = ', ans)

                except Exception as e:
                    print('GC: *', tc_input + ': exception: ' + str(e))

                # Grade result if run_complete
                if run_complete:

                    tc_score = P['score']/num_tc
                    # print('debug: tc_score = ', tc_score)

                    try:
                        prc = subprocess.run([grader_command,
                            P['grader'], rout, ans, str(tc_score),
                                              P['Px'], log_file],
                            input=None, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, timeout=1)

                        grading_out = str(prc.stdout, 'utf-8')
                        print('GC: * grading ', grading_out)
                        point += float(grading_out)
                    except Exception as e:
                        print('GC: *', P['grader'] + ': exception: ' + str(e))

            graded[P['Px']] = round(point)

            # Clean up/Remove student file
            print('GC: * Done: clean up {}'.format(P['student']))
            try:
                os.remove(P['student'])
            except Exception as e:
                print('** clean up fails: ', e)

        else:
            print('GC: * %s is NOT submitted' % P['student'])
            graded[P['Px']] = 0

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
        print('GC: grader (%s) log file'%P['grader'])
        print(m)
        print("\n\n")


    # Print score text (must at the end)
    #print(score_txt)
    #print('{"scores": {"P1": 5, "P2": 5},"scoreboard":[5, 5, 10]}')
    return score_txt

if __name__ == '__main__':

    grader_paths = {'student': './student',
             'answer': './answers',
             'working': '.',
             'log_file': './glog.txt',
             'student_email_json': './settings.json',
             'student_vfile': './student/verify.txt'}

    # MODE
    # 'Autolab' for running on Autolab server
    # 'Test' for single submission test (student folder) on PC
    # 'Local Batch' for running downloaded all submissions on PC

    # MODE = 'Autolab'
    MODE = 'Test'
    # MODE = 'Local Batch'

    # verified = True # for exam
    verified = False # normal exercises

    print('GC: MODE =', MODE)

    load_identity = False
    # Identify reflection
    try:
        with open(grader_paths['student_email_json'],
                  encoding='utf-8', mode='r') as f:
            jsontxt = f.read()

        d = json.loads(jsontxt)
        print('GC: identity =', d['user'])

        if verified:
            if not verify(d['user'],
               read_student_verf(grader_paths['student_vfile']),
               codebookf):
                print('Verification failed!')
                print('Verification code does not match!')
                exit(0)

    except Exception as e:
        print('GC: identity check: exception:', e)
        if verified:
            print('GC: verifying mode: cannot verify identity')
            exit(0)



    # CPG Class
    # runtest_cmd = 'g++'
    # runtest_suffix = '-o runtest.exe; ./runtest.exe'

    # FCP Class
    # runtest_cmd = 'python3.5'
    runtest_cmd = 'python'
    runtest_suffix = ''


    if MODE == 'Autolab':
        directive_file = sys.argv[1]
        python_cmd = 'python'

        # Run grader
        rst = run_grader(directive_file, runtest_cmd, runtest_suffix, python_cmd, grader_paths)

        print(rst)

    elif MODE == 'Test':
        directive_file = "./answers/ans.txt"
        python_cmd = "python"

        rst = run_grader(directive_file, runtest_cmd, runtest_suffix, python_cmd, grader_paths)

        print(rst)

    elif MODE == 'Local Batch':

        directive_file = "./answers/ans.txt"
        python_cmd = "python"

        # Grading directory
        tar_dir = './tars'
        untar_dir = grader_paths['student']

        # Graded result file
        grade_file = 'graded_results.txt'

        # List all tar submissions to be graded
        tar_files = os.listdir(tar_dir)
        print('Total', len(tar_files), 'files')


        #######################################################
        # Go through each tar: untar, grade, and save result
        #######################################################

        graded_results = ''

        for f in tar_files:

            sid = f.split('.')[0].strip()

            p = os.path.join(tar_dir, f)
            print(p)

            # Clean the target folder
            clean_folder(untar_dir, confirm=False)

            # Untar
            try:
                zf = tarfile.TarFile(p, 'r')
                zf.extractall(untar_dir)
                zf.close()
            except Exception as e:
                graded_results += sid + ";" + str(e) + '\n'
            else:
                # Untar successful
                # Run grader
                rst = run_grader(directive_file, runtest_cmd, runtest_suffix, python_cmd, grader_paths)

                graded_results += sid + ";" + str(rst) + '\n'

        print(graded_results)

        with open(grade_file, 'w') as grade_f:
            grade_f.write(graded_results)
