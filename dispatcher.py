"""
Predecessor: grader_center4.py
Updated: Apr 24th, 2021
Added:
* handling embedded form: a single json txt with all answers (to do ....)

Obtained from grader_center4.py:
(1) accommodating C++ (compilation and run)
(2) refactoring code
(3) allowing easier debugging
(4) allowing explanation option
(5) allowing  flexible runtest command

==================================================
Calling Scenarios:
  (1) main: python3.5 dispatcher.py "./cfg/eval.cfg" -autolab
  (2) exam: python3.5 dispatcher.py "./cfg/eval.cfg" -autolab -verified
  (3) embedded form: python3.5 dispatcher.py "./cfg/eval.cfg" -autolab -json
  (4) exam with e.form: python3.5 dispatcher.py "./cfg/eval.cfg" -autolab -json -verified
  (5) batch: python dispatcher.py
    (batch uses default cfg.)
  (6) batch for exam: python dispatcher.py "./cfg/eval.cfg" -verified
    * should be well taken care, since the verification is done in run_grader
    * BUT, this has not been tested yet!

  * The evaluation configuration "eval.cfg" must be the first argument.
  But, directives -autolab, -json, and -verified can be put in any order after "eval.cfg".

  Note: 
  * There is no combination of -batch and -json, since batch mode is used only when Autolab server is down.
  When the server is down, it is awkward to have students write their answers in json.
  
==================================================
Key Assumptions:
1. student's submission: ./student (see paths if change)
    It copies only "target" files to its working directory to grade.
    (This is to safeguard against accidental write over grader files.)
    The "target" files are specified in the directive file, e.g., ans.cfg.
2. sys.argv[1]: a directive file indicating Problem #, Points, Student Submission File, etc.
3. Identity verification option
    Student's identity of the submission is provided in settings.json
    (through secret code defined in a secret function)
    3.1 Run gen_emailcode('email file', 'output_email_code_file')
        to get the email-code pairs.
        See D:\Classes\00FCP\2019b\L00a\local_autograde\sandbox1 for example.
        E.g., gen_emailcode('email_list.txt', 'emailcode.txt')
    3.2 Hand codes to students, personally.
    3.3 Ask students to put the secret code in a verify file, e.g., verify.txt.
    3.4 Include verify.txt in the tar file
=============================
Tested:

* batch mode: python dispatcher.py
* autolab main: python3.5 dispatcher.py "./cfg/eval.cfg" -autolab
* exam: python3.5 dispatcher.py "./cfg/eval.cfg" -autolab -verified
* embedded form: python dispatcher.py "./cfg/eval2021g.cfg" -autolab -json

"""

import os
import sys
import tarfile
import json
import time

# For running the submission and getting the output
from runtest_tool import clean_folder, run_grader, json_grader

if __name__ == '__main__':

    print("\ndispatcher.py: current time = ", time.ctime())

    grader_paths = {'student': './student',
             'answer': './answers',
             'working': '.',
             'log_file': './glog.txt',
             'student_email_json': './settings.json',
             'student_vfile': './student/verify.txt'}

    # For a local batch mode
    BATCH_TAR_DIR = '../tars'
    BATCH_GRADE_FILE = '../graded_results.txt'

    # For a json format
    STUDENT_JSON = "student.json"

    '''
    Default settings
    MODE
        * autolab: running on Autolab server
        * batch (default): running in a batch mode (going over multiple students) on a local machine 
    STUDENT_FORMAT
        * multiple (default): student's submissions are seen in multiple files, which packaged together (in a tar file)
        * json: student's submissions are seen in single json text file, from an embedded form
    VERIFIED
        * False (default): no identity verification
        * True: identity verification is enforced
    '''

    MODE = 'batch'                  # in case the server down
    STUDENT_FORMAT = 'multiple'     # each P has its on student's answer
    VERIFIED = False                # for exercises/homework
    DIRECTIVE_CFG = "./cfg/eval_win.cfg"    # Directive cfg file

    #########################################
    # Assign settings to calling arguments
    #########################################

    if '-autolab' in sys.argv:
        MODE = "autolab"
        DIRECTIVE_CFG = sys.argv[1]

        # Note: batch mode uses a default DIRECTIVE_CFG.

    if '-json' in sys.argv:
        STUDENT_FORMAT = "json"
        assert MODE == "autolab", \
            "Local batch mode is not prepared for a json format."

    if '-verified' in sys.argv:
        VERIFIED = True

    print("dispatcher: Running mode = ", MODE)
    print("dispatcher: Submission format = ", STUDENT_FORMAT)
    print("dispatcher: Individual code verification = ", VERIFIED)

    if MODE == 'autolab':
        # Run grader
        rst = ""
        if STUDENT_FORMAT == 'json':

            student_submission = os.path.join(grader_paths['student'], STUDENT_JSON)
            rst = json_grader(student_submission, DIRECTIVE_CFG, grader_paths, codeverify=VERIFIED)

        else:
            # STUDENT_FORMET == 'multiple' (tar file)

            rst = run_grader(DIRECTIVE_CFG, grader_paths, codeverify=VERIFIED)
        # end if STUDENT_FORMAT

        print(rst)

    else: # MODE == 'batch'
        print("dispatcher: Local batch run over every student's submission in ", BATCH_TAR_DIR)
        print("dispatcher: Local batch run: the graded results will be put in", BATCH_GRADE_FILE)

        # List all tar submissions to be graded
        tar_files = os.listdir(BATCH_TAR_DIR)
        print('dispatcher: Local batch run: Total', len(tar_files), 'files')

        # Grading directory
        untar_dir = grader_paths['student']

        #######################################################
        # Go through each tar: untar, grade, and save result
        #######################################################

        graded_results = ''

        # Go over every tar files
        for f in tar_files:

            sid = f.split('.')[0].strip()

            p = os.path.join(BATCH_TAR_DIR, f)
            print("\n", p)

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
                rst = run_grader(DIRECTIVE_CFG, grader_paths, codeverify=VERIFIED)

                graded_results += sid + ";" + str(rst) + '\n'
            # end try-except-else untar
        # end for f in tar_files

        print(graded_results)

        with open(BATCH_GRADE_FILE, 'w') as grade_f:
            grade_f.write(graded_results)

    # end if-else

# end if __name__ == '__main__'