"""
Created on Apr 22nd, 2021 
Adapted from extDynamicGrader2.py (for LCA2021 FE FE0)
* customized for processing thai message (comparing against thai-ref text in 'utf-8' coding)
    * it reads the student json file itself. (cfg["submission"])
        * This is to avoid hassle of passing thai text as a command argument (doing so causes error on subprocesss, used in cmd_tool.cmd).
    * it extracts student's thai text from key, specified by cfg["thai-qid"].
    * it reads the thai-ref text from a file, whose name is from cfg["thai-ref"].
    * Then, compare Thai submission text against the Thai ref text.
    * If they are matched, proceed to English text, which eventually leads to conditional dynamic message.
        * if score > 0 (both Thai and English texts are matched their references), show the message a/t email.

Attempt and fail!
    * sys.stdout.buffer.write(ttext.encode('utf-8'))
    It seems OK running on its own, 
    but when the entire program was run through subprocess (cmd_tool.cmd), it gives UnicodeEncodeError.
    ** This tanks my desire to display thai alphabets on Autolab feedback. It didn't even get pass my own python code. Let alone have its display correctly on the server.
    ** So, display Thai on Autolab feedback FAILED
    *** What I can do is still to check thai text against ref (of course in 'utf-8' aka as bytes)
    ** This means that I cannot do it through external policy. I can try it with an internal policy, but it causes too much trouble with too little provable effect.
"""

import sys
import json
import os
from policy2021 import numtol_policy2
from misc_tools import unpack_message
import time
from emform_tools import read_form, clean_unicode
import extDynamicGrader3 as dg


if __name__ == '__main__':

    # print("Debug: extCustomJsonTE1: sys.argv=", sys.argv)

	# Default/test values
    params = {"policy": "extCustomJsonTE1.py",
                "config": "./cfg/ecjte1FE0.cfg", # configuration file---cmd to generate ref and msg
                "score": 1,    # full score
                "mode": "Show", # reporting mode
                "student": "",
                "mainref": None}

    var_list = ["policy",   # this policy
                "config",   
                "score",    # full score
                "mode"     # report mode: "Show"/"Silence"/"HidNum"
    ]

    for i, arg in enumerate(sys.argv):
        params[var_list[i]] = arg
    # end for

    ########################
    # Read its cfg
    ########################

    with open(params['config'], 'r') as f:
        cfg_txt = f.read()
        cfg = json.loads(cfg_txt)

    ########################
    # Read student json
    ########################

    try:
        student_all = read_form(cfg["submission"])

    except Exception as e:
        print("extCustomJsonTE1.py: student\'s answers (json) load error:", e)
        print(0)
        exit(0)
    # end try-except    

    #########################################
    # Extract thai text of the submission
    #########################################

    thai_text = student_all[cfg["thai-qid"]]
    list_thai = thai_text.split(';')[:-1]

    # print(thai_text)
    # print(list_thai)

    #########################################
    # Extract thai reference
    #########################################
    f = open(cfg["thai-ref"], encoding='utf-8', mode='r')
    utf8_ref = f.read()
    f.close()

    thai_ref = clean_unicode(utf8_ref)
    list_thairef = thai_ref.split(';')[:-1]

    # print(thai_ref)
    # print(list_thairef)

    #############################################
    # Compare thai submission against thai ref
    #############################################

    Nsub = len(list_thai)
    Nref = len(list_thairef)
    Nmin = min(Nsub, Nref)

    match = True
    mismatch_index = 0
    for i in range(Nmin):
        if list_thai[i] != list_thairef[i]:
            match = False
            mismatch_index = i
            break
    # end for i

    if match and (Nsub != Nref):
        match = False
        i += 1
        
    TH_score = match * float(params["score"])/2

    print("{}: Thai score =".format(params['policy']), TH_score, end=' ')

    if match:
        print("(perfect match)")
    else:
        print("\n{}: Thai text mismatch at index: {}".format(params['policy'], i))
    
    #############################################
    # Check the english submission
    #############################################

    # Extract english text of the submission
    eng_text = student_all[cfg["eng-qid"]]

    # Extract english reference
    f = open(cfg["eng-ref"], encoding='utf-8', mode='r')
    eng_utf8_ref = f.read()
    f.close()

    eng_ref = clean_unicode(eng_utf8_ref)

    # print(eng_text)
    # print(eng_ref)

    # Compose parameter dict for makeandgrade
    cfg["make-ref"] = "no" # Fixate to thai and english texts. No dynamic ref!

    dgparams = {"policy": "(dynamic grader)",
        "dynamic-config-dict": cfg,
        "score": float(params["score"])/2,    # English score
        "offset": TH_score,
        "mode": params["mode"],
        "student": eng_text,
        "mainref": eng_ref}

    Total_score = dg.makeandgrade(dgparams)

    print("Total score:")
    print(Total_score, end='')

