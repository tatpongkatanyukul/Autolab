"""
Created on Apr 24th, 2021 
Adapted from extDynamicGrader2.py (for LCA2021 FE FE0)
* extDynamicGrader1.py: dynamically generates reference and post-messages
* extDynamicGrader2.py: shows post-messages on condition
* This adaptation: re-engineer extDynamicGrader2.py so that makeandgrade takes a dict of parameters
with dynamic information readily provided.
    * This allows a cleaner re-use of makeandgrade from other modules, e.g., extCustomJsonTE1.py
    * makeandgrade also checks on policy_par["offset"], so that it allows combines score for post-message condition.
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

    if "offset" not in policy_par:
        policy_par["offset"] = 0

    # Read dynamic params
    cfg = {}
    if "dynamic-config-dict" in policy_par:
        cfg = policy_par["dynamic-config-dict"]

    # Default values
    default_val = {"lookup": "./dynamic/AMlookup.txt",
                    "selector": "settings.json",
                    "make-ref": "yes",              # if "no", use policy_par["mainref"]
                    "make-post-msg": "conditional", # "yes"/"no"/"conditional"
                    "condition": ["gt", 0],         # only valid for make-post-msg == "conditional"
                    "numtol": 0.05}

    for k in default_val:
        if k not in cfg:
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

    student_score += policy_par["offset"]

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


if __name__ == '__main__':

    # print("Debug: extDynamicGrader3: sys.argv=", sys.argv)

	# Default/test values
    params = {"policy": "extDynamicGrader3.py",
                "config": "./cfg/edg3FE0.cfg", # configuration file---cmd to generate ref and msg
                "score": 0.5,    # full score
                "mode": "Show", # reporting mode
                "student": """I will and always comply with Khon Kaen University's code of conduct and academic integrity policy. I will take this exam with honor and honesty.""",
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
        params[var_list[i]] = arg
    # end for

    #################################
    # Read dynamic cfg
    #################################

    with open(params['config'], 'r') as f:
        cfg_txt = f.read()
        cfg = json.loads(cfg_txt)

    params["dynamic-config-dict"] = cfg

    ################################################################
    # Make dynamic reference, grade, and make dynamic post-message
    ################################################################

    score = makeandgrade(params)

    print("Score:")
    print(score, end='')