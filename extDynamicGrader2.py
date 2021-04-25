"""
Created on Apr 21st, 2021 
Adapted from extDynamicGrader1.py (for LCA2021 FE FE0)
* Add conditional post-messaging
    makeandgrade handles its cfg file, e.g., edg1FE0.cfg, with more options of "make-post-msg", i.e.,
    "no": post-message = "",
    "yes": post-message is made according to a lookup file and a selector key,
    "conditional": when CONDITION is met, a post-message is made (a/t lookup and selector)
    The CONDITION is specified with "condition" in the cfg file.
    "condition": show when score meets the condition 
    * ["lt", threshold], e.g., "condition": ["lt", 30], show when score < 30.
    * ["gt", threshold], e.g., "condition": ["gt", 50], show when score > 60.
    * ["eq", threshold], e.g., "condition": ["eg", 0], show when score == 0.
    Default is to show when score > 0, i.e., "condition": ["gt", 0]


It is intended for LCA 2021 Online FE.

To facilitate dynamic grading and post messaging.
This would allow:
* personalized questions: different students can work on different sets of questions
and their answers are graded accordingly.
* Also, the post messages, which will be shown after the grading is complete.

Grading based on numtol2 (policy2021.numtol_policy2).

It personlizes a reference text and post message specified in the look-up table (in csv w/ comman delimiters).
The look-up table is in the following format:
    e-mail, student_id, pattern, num_vals, v1,v2,...,vN, msg_pattern, num_vals, v1,v2,...,vM
    tatpong@kku.ac.th,623040001-8, ./dynamic/A1a.pat, 3, 1, 2, 4, ./dynamic/M1a.pat, 2, 100, 150

That is, column 3 is the reference pattern, followed by a number of values associated with it, 
and the actual values in order.
Then, depending on how many reference values, the post message pattern, its number of values, and values.
Having this structure, each student can have one's own pattern and a set of values, it even allows a different number of values.
"""

import sys
import json
import os
from policy2021 import numtol_policy2
from misc_tools import unpack_message
import time


def make_txt(pat_file: str, values: list):
    """
    Take pattern file---pat_file---, put values into the pattern, and return the text.
    Call:   make_txt("A1a.pat", ["1", "2", "4"])
    """

    with open(pat_file, 'r') as f:
        pattern = f.read()
    
    text = pattern.format(*values)

    return text
# end make_txt

def look_up(selector_key, LU_fname):
    '''
    Look for each in the content of file, named by LU_fname
    to find the contents whose first token matches the selector_key.
    Call:
        look_up("tatpong@kku.ac.th", "AMLookUp.txt")

    Note: it is adapted from verify_mod.codebookf
    '''

    matched_content = None

    with open(LU_fname, 'r') as f:
        for line in f:
            line_tokens = line[:-1].split(',')
            if line_tokens[0].strip() == selector_key:
                matched_content = line_tokens
                break
    
    # Clean extra spaces
    if matched_content is not None:
        for i in range(len(matched_content)):
            matched_content[i] = matched_content[i].strip()
            

    return matched_content
# end look_up

def makeandgrade(policy_par):

    # Read configuration file
    with open(policy_par['config'], 'r') as f:
        cfg_txt = f.read()
        cfg = json.loads(cfg_txt)

    # Default values
    default_val = {"lookup": "./dynamic/AMlookup.txt",
                    "selector": "settings.json",
                    "make-ref": "yes",
                    "make-post-msg": "yes",
                    "condition": ["gt", 0],
                    "numtol": 0.05}

    for k in default_val:
        if k in cfg:
            continue

        cfg[k] = default_val[k]
    # End for default_val

    ########################
    # Get selector_key
    ########################
    with open(cfg['selector'],
                encoding='utf-8', mode='r') as f:
        selector_json = f.read()

    d = json.loads(selector_json)

    selector_key = d[cfg['selector-key']]

    ########################################
    # Read ref and msg patterns and values
    ########################################

    dynamic_tokens = look_up(selector_key, cfg["lookup"])

    f_ref = 2   # an index of ref pattern field
    ref_pattern_fname = dynamic_tokens[f_ref]
    N = int(dynamic_tokens[f_ref + 1]) # a number of values
    i_ref = f_ref + 2 # an index of the first ref value
    ref_vals = dynamic_tokens[i_ref:(i_ref + N)]
    
    f_msg = i_ref + N # an index of msg pattern field
    msg_pattern_fname = dynamic_tokens[f_msg]
    M = int(dynamic_tokens[f_msg + 1]) # a number of values
    i_msg = f_msg + 2 # an index of the first msg value
    msg_vals = dynamic_tokens[i_msg:(i_msg + M)]

    #==========================
    # Generate reference text
    #==========================

    ref_txt = policy_par["mainref"]

    if cfg["make-ref"] == "yes":

        ref_txt = make_txt(ref_pattern_fname, ref_vals)

    #===============================================
    # Grade student's answers against the reference
    #===============================================

    # Grade the output based on reference
    student_score = numtol_policy2(policy_par["student"], ref_txt, 
        float(policy_par['score']), policy_par["mode"], float(cfg["numtol"]), neg_handling=True)

    print("{}: Grading is complete: score = {}".format(policy_par["policy"],student_score))
    #================================
    # Generate post-grading message
    #================================

    post_msg = ""
    eps = 0.1

    if cfg["make-post-msg"] == "yes":

        post_msg = make_txt(msg_pattern_fname, msg_vals)
        print(post_msg)

    elif cfg["make-post-msg"] == "conditional":
        condition = cfg["condition"]
        if (condition[0] == "gt") and (student_score > float(condition[1])):
            post_msg = make_txt(msg_pattern_fname, msg_vals)
            print(post_msg)

        elif (condition[0] == "lt") and (student_score < float(condition[1])):
            post_msg = make_txt(msg_pattern_fname, msg_vals)
            print(post_msg)

        elif (condition[0] == "eq") and \
            (float(condition[1]) - eps <= student_score <= float(condition[1]) + eps):
            post_msg = make_txt(msg_pattern_fname, msg_vals)
            print(post_msg)
        else:
            print("{}: Condition is not met (score {} {}): post-msg is suppressed.".format(policy_par["policy"], condition[0], condition[1]))

    return student_score
# end makeandgrade

def progressive_tests():

    print("\nTest make_text:")
    print("current path:", os.getcwd())
    print("\nA1a.pat\n", make_txt("A1a.pat", ["1", "2", "4"]), sep='')
    print("\nA1b.pat\n",make_txt("A1b.pat", ["8", "9", "10"]), sep='')
    print("\nM1a.pat\n", make_txt("M1a.pat", ["100", "150"]), sep='')
    print("\nM1b.pat\n",make_txt("M1b.pat", ["1k"]), sep='')
    print()

    print("\nTest look_up:")
    print("tatpong@kku.ac.th\n", look_up("tatpong@kku.ac.th", "AMlookup.txt"))
    print("\ntatpong@gmail.com\n", look_up("tatpong@gmail.com", "AMlookup.txt"))
    print("\njiradej@kku.ac.th\n", look_up("jiradej@kku.ac.th", "AMlookup.txt"))
    print("\nnoone@kku.ac.th\n", look_up("noone@kku.ac.th", "AMlookup.txt"))

# end progressive_tests



def test():
    student = """Q1.1. v(t) = -10.000 exp( -500.000 t) + 10.000 V
Q1.2. v = 5.276 V
Q1.3. Vx = 9.975 angle 1.57
Q1.4. Vx(t) = 9.975 cos( 612 t + 1.57 ) V
Q1.5. zx = 120 + j 85.5"""
# end test()

if __name__ == '__main__':

    # print("Debug: extDynamicGrader1: sys.argv=", sys.argv)

	# Default/test values
    params = {"policy": "extDynamicGrader2.py",
                "config": "./cfg/edg1FE0.cfg", # configuration file---cmd to generate ref and msg
                "score": 60,    # full score
                "mode": "Show", # reporting mode
                "student": """I will and always comply with Khon Kaen University's code of conduct and academic integrity policy. I wil take this exam with honor and honesty.""",
                "mainref": """I will and always comply with Khon Kaen University's code of conduct and academic integrity policy. I will take this exam with honor and honesty."""}

    var_list = ["policy",   # this policy
                "config",   
                "score",    # full score
                "mode",     # report mode: "Show"/"Silence"/"HidNum"
                "student",
                "mainref"]

    for i, arg in enumerate(sys.argv):
        if (i == 4) or (i == 5):
            arg = unpack_message(arg)
            #print("extDynamicGrader1: student's answer:")
            #print(arg)
        params[var_list[i]] = arg
    # end for
    # print("Debug: extDynamicGrader1: params=", params)

    score = makeandgrade(params)

    print(score, end='')

