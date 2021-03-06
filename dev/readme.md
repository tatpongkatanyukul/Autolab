# OVERVIEW

![OVERVIEW](https://github.com/tatpongkatanyukul/Autolab/raw/main/dev/autograde.png)


# Apr 21st, 2021. ([dev/2021h](https://github.com/tatpongkatanyukul/Autolab/raw/main/dev/2021h.tar))
  * fix dev/2021g on ```numgraders.is_number``` (fix regular expression to differentiate "2" and "2.0" from "2.")
    * before: ```line 2``` will be matched to ```line 2.``` (Actually, it's not that bad)
    * after: ```line 2``` will be caught that it misses period at the end. 
  * enable post-message scheme based on score: ```extDynamicGrader3.py``` (adapted from ```extDynamicGrader2.py``` to have a cleaner ```makeandgrade```)
    * specify in its json cfg key: ```"make-post-msg"```
      * "no": post-message = "",
      * "yes": post-message is made according to a lookup file and a selector key,
      * "conditional": when CONDITION is met, a post-message is made (a/t lookup and selector). The CONDITION is specified with key "condition" in the cfg file. 
        * Key ```"condition"```: 
          * ["lt", threshold] means that score < threshold, e.g., 
          ```"condition": ["lt", 30]```, show when score < 30.
          * ["gt", threshold] means that score > threshold, e.g., 
          ```"condition": ["gt", 50]```, show when score > 60.
          * ["eq", threshold] means that score == threshold, e.g., 
          ```"condition": ["eg", 0]```, show when score == 0.
          * Default (when there is no key "condition") is to show when score > 0, i.e., 
          ```"condition": ["gt", 0]```
    
  * a custom external policy: ```extCustomJsonTE1.py```
    * This is customized to LCA2021 FE0 for Thai and English Integrity Declaration 
    * It reads json, gets both Thai and English texts, compares Thai text against reference, then check the English one. It adds both Thai and English scores together, show the dynamic message on condition. (It is flexible so that I can choose either to have them both correct (i.e., condition: ["gt", 1]) or to have one of them correct (i.e., condition: ["gt", 0]).
      * It achieves conditional post-message display through ```extDynamicGrader3.makeandgrade``` 
  * fix handling ```-verified```, so that both ```runtest_tool.run_grader``` and ```runtest_tool.json_grader``` can do personal code verification.
    * codebook: ```codebook.csv```
    * student's code
      *  must be put in ```verify.json``` when run in ```multiple``` input mode (without ```-json```, run ```runtest_tool.run_grader```)
        * verification has been moved from ```dispatcher.py``` to ```runtest_tool.py```  
      *  must be filled in a textarea (or input) with id ```checkcode``` when run in ```json``` ((with ```-json```, run ```runtest_tool.json_grader```)
  * fix ```runtest_tool.get_Grading_Table``` to allow more flexible writing on the main evaluation cfg.
  * remove policy ```external-forward``` (from ```runtest_tool.grading```), since it does not seem to do anything ```external``` cannot except allow the evaluation code to be put in the cfg main run field. 
  * tweak ```cmd_tool.cmd``` a little bit, so that when command-to-run gets too long, it displays just enough, but not to clutter over multiple lines.



# Apr 19th, 2021. (dev/2021g)

* [Autograder2021g](https://github.com/tatpongkatanyukul/Autolab/raw/main/dev/autograder2021gA5Q2.tar)
  * **Dynamic Grading** and **dynamic post-grading messaging** (used as a primitive dynamic question delivery)
    * Use in A5Q1 (dynamic post messaging) and A5Q2 (both dynamic grading and post messaging)
    * Key components: ```extDynamicGrader1.py``` (with little help from ```misc_tools.py```)
  * Also, nicer display ```extpolicy4.py``` adapted from ```extpolicy3.py``` to prefix each line of its delegated program (making it easier to read, see output from ```numtol_policy2```) and options to show pre-run and post-run details even when there is no error (perhaps, not much use for now).
  * ```extLCAjson0.py``` (temporary) an adaptor so that json input can be also read in ```run_grader```
    * A more efficient way is to use ```json_grader``` 

## Overview
![Overview](https://github.com/tatpongkatanyukul/Autolab/raw/main/dev/autograder2021g.png)

## Scenarios

### Python (original and simplest case)
![Python Scenario](https://github.com/tatpongkatanyukul/Autolab/raw/main/dev/ScenarioPython.png)

### Identity Verification
![Identity Verification](https://github.com/tatpongkatanyukul/Autolab/raw/main/dev/ScenarioVerify.png)

### C++
![C++ Function  CPG2021 M002 Function Scenario](https://github.com/tatpongkatanyukul/Autolab/raw/main/dev/ScenarioExternalCPPFunctions.png)

### Dynamic Messaging
![Dynamic Messaging LCA2021 A5Q1 Scenario](https://github.com/tatpongkatanyukul/Autolab/raw/main/dev/ScenarioDynamicMsg.png)

### Dynamic Grading
![Dynamic Grading LCA2021 A5Q2 Scenario](https://github.com/tatpongkatanyukul/Autolab/raw/main/dev/ScenarioDynamicGrading.png)

***WARNING!!!***
  * ```AutolabJudge``` and its related policies, e.g., ```extLCA1```, ```extLCAjson1```, should be used with extreme ***caution***, since  ```AutolabJudge``` has been found to have an issue with tolerance in its "equation" mode (including anything with function, e.g., ```Q2.1: -10 + Vx - 100 ix = 0```, ```Q2.2: v(t) = -10 exp( -500 t) + 30```, ```Q2.3. i(t) = 0.01 cos( 677 t + 1.57 )```, and ```Q2.4. Vx = 3 angle 1.57```).

Key (intended) additions
  * fix ```json_handler``` and its associcated codes, so that ```python dispatcher.py -autolab -json``` and ```python dispatcher.py -autolab -json -verified``` work
    * Done! tested using ```python dispatcher.py "./cfg/eval2021g.cfg" -autolab -json````
    with cfg = ```Q1\; 60\; student.json\; dummy \; 0\; numtol2\; 0.01\; HidNum\; dummy.txt Q1.ans``` 
  * add personalized grading policy, i.e., given a student's email (obtained from ```settings.json```), grader selects an associated reference text to compare against.
    * this allows a personalized exercise, where a student gets one's own questions different from other students and one's answers are graded accordingly.
  * add personalized post message feature, i.e., after grading student's submission, a grader give out a personalized message along with scores and other comments.
    * this personalized post message feature can be exploited as a primitive question delivery, where a post message could be a next question information

## Design Dilemma
### Premise
  * grading policy: ```external``` leads to execution of a value of the cfg field ```GAttrib```
    * ```P108b\; 60\; P108.cpp\;   \; 0\; external\; python3.5 extpolicy3.py ./cfg/ext2P108.cfg; 360\; HidNum\; ```
    * note: the cfg 4th and 5th fields ```Run``` and ```Runtime``` are put a dummy ``` ```. If we need, we can put another code in.
      * ```P1\; 60\; P1.cpp\; python3.5 test_submission.py ./info.txt P1.cpp \; 120\; external\; python3.5 extGrader.py ./cfg/extP1.cfg; 360\; HidNum\; ``` (```test_submission.py``` and ```extGrader.py``` are fictitious names)
    * **caution!** 
      * the cfg field ```GAttrib``` has 2 parts: [_code to be run_];[_max run time_]
      * [_code to be run_] is added with [_score_] and [_reporting mode_], i.e., what will be executed is: [_code to be run_] [_score_] [_reporting mode_]
        * E.g., for GAttrib: ```python3.5 extGrader.py ./cfg/extP1.cfg; 360```, the code ```python3.5 extGrader.py ./cfg/extP1.cfg 60 HidNum``` will be executed. The score and reporting mode are attached automatically from the cfg 2nd and 8th fields, ```Points``` and ```Report```. 
  * grading policy: ```external-forward``` just forward the output of the cfg field ```Run``` execution (along with feedback if ```mode != 'Silence'```)
    * ```P1\; 60\; P1.cpp\; python3.5 test_and_grade_submission.py ./info.txt\; 360\; external-forward\; none\; HidNum\; dummy.txt dummy.txt``` (```test_and_grade_submission.py``` is a fictitious name)
    * Unlike ```external```, the ```external-forward``` renders the cfg fields ```GAttrib``` irrelevant (completely ignored).
 ### Discussion
   * Logically, the cfg 4th field ```Run``` should be providing the submission output and the cfg 6th field ```Grader``` (along with ```GAttrib```) should compare the submission output against the reference output and decide the grade.
     * So far, ```external-forward``` is slack on this and combine both obtaining submission output and grading output conferring with reference into a single run, e.g., ```extpolicy3.py```, ```extLCA1.py```, and ```extLCAjson0```.
     * ```external``` policy itself does not really violate this logic, but the way I use it, i.e., with ```extpolicy3.py```, ```extLCA1.py```, and ```extLCAjson0```, is combining both tasks into one single run, e.g., ```extpolicy3.py``` does everything inc. obtaining submission output, loading reference, and exploying ```numtol_policy2``` for grading.
   * In dynamic (personalized) question setting, the reference itself has to be dynamic

# Apr 16th, 2021. (dev/2021f)

**WARNING!** ```json_handler``` (option ```-json```) is half baked. It is not even finished yet.
  * However, related external policies, e.g., ```extLCAjson0.py``` has been tested using ```run_grader``` (See dev/2021g for the latest development): tested by ```python dispatcher.py``` with cfg: ```Q4\; 60\; student.ans\; python3.5 extLCAjson0.py student.ans Q4 ./answers/Q4.ans 0.01 60 HidNum\; 30\; external-forward\; none\; HidNum\; dummy.txt dummy.txt```

Major changes
  * Get rid of unnecessary routing: ```autograde-makefile``` -> ```driver.sh``` -> ```grading_center4.py``` -> ```runtest_tools.py```
    *  ```autograde-makefile``` -> ```dispatcher.py``` (adapted from ```grading_center4.py```) -> ```runtest_tools.py```
    *  no ```driver.sh``` and the 2nd makefile anymore
  * Add policy ```external-forward``` 
    * so that instead of using ```external``` policy and put code into policy attributes, we can put code into the run field of the cfg directly
    That is,
    instead of
```
P108\; 60\; P108.cpp\;   \; 0\; external\; python3.5 extpolicy3.py ./cfg/ext2P108.cfg; 360\; HidNum\; 
```
    now we can do
```
P108\; 60\; P108.cpp\; python3.5 extpolicy3.py ./cfg/ext2P108.cfg 60 HidNum\; 360\; external-forward\; none\; HidNum\; dummy.txt dummy.txt
```
It may look a bit longer in the cfg, but internally it works cleaner (in my opinion). But, both external and external-forward are valid. So, use whichever style you like.
  * Add policy ```extLCA1.py``` so that LCA-like answers in a tar file can be nicely graded with Peraphol's ```AutolabJudge```
  * Add policy ```extLCAjson1.py``` so that LCA-line answers in a json file (from an embedded form) can be graded with Peraphol's ```AutolabJudge```. Also policy ```extLCAjson0.py``` using ```numtol2``` is added.
    * This can work as an external policy (or external-forward policy), i.e., it can be configured as:
```
Q1\; 60\; student.ans\; python3.5 extLCAjson1.py student.ans Q1 ./answers/Q1.ans 0.01 60 HidNum\; 30\; external-forward\; none\; HidNum\; dummy.txt dummy.txt
```
Although this approach works, but it is a little bit inefficient, as it loads a json file and parses it every question. 
It will be more efficient if we can load and parse a json file once and go over every answers in it. That's the another addition, the ```json_grader```
  * Add ```json_grader``` for efficient parsing of json from an embedded form, along with modification to ```dispatcher.py``` to properly invoke ```json_grader``` for a json file from an embedded form or ```run_grader``` for a tar file
    * ```json_grader``` loads and parses a json file once, then goes over questions specified in the cfg.
  * Modify ```dispatcher.py``` to accommodate both ```json_grader``` and ```run_grader``` as well as having arguments: ```-autolab```, ```-verified```, and ```-json```
    *  ```-autolab``` for running this ```dispatcher.py``` in the autolab server, i.e., student's submissions have been nicely put in folder ```student```
      * if no ```-autolab```, ```dispatcher.py``` will run in a batch mode, i.e., taking a tar file from folder ```../tars``` one by one and grade each one with ```run_grader```
    * ```-verified``` for identity verification, checking contents of student's ```verify.txt``` against what specified in ```codebook.txt```
    * ```-json``` for an embedded form, ```dispatcher.py``` will invoke ```json_grader``` to handle the input

  * Change names:
    * ```grading_center4.py``` to ```dispatcher.py```
    * policy names
      * ```Deploy``` to ```Silence```
      * ```Test``` to ```Show``` 
  * Integrate:
    * ```graders.grading(...)``` into ```runtest_tools``` (no ```graders.py``` anymore) 
  * Tidy up the starting makefile
    * add ```> /dev/null``` to the end of ```tar xvf autograde.tar``` so that the feedback seems cleaner
    * also, integrate what ```driver.sh``` and its makefile had done, so that I can tidy up the pipeline (get rid of ```driver.sh```)

Pressing needs that I have not addressed yet!
  * grader with hint, instead of telling score, give out some message
  * personalized grader, i.e., the answer for each problem does not have to be fixed. The question may be personalized to each student and the answer should be able to reflect that
    * along with this, I need a more efficient way for question delivery (a dynamic option, of course, where I can code to generate a question based on student's email) 

![Autograder 2021f](https://github.com/tatpongkatanyukul/Autolab/raw/main/dev/autograder2021f2.png)

## Intermediate stage
[Autograder](https://github.com/tatpongkatanyukul/Autolab/raw/main/dev/autograder.png)

Key components:  
  * ```grader_center4```: (```autograde-makefile``` -> ```driver.sh``` -> ```grader_center4.py```) starting point of the python autograder
    * It is actually more like a **dispatcher**. It is an adapter for ```runtest_tool.run_grader(...)```, i.e., prepare proper directive for both autolab run or local batch run and acts as autolab management (going through every student's submission) for local batch run
    * It also performs identify verification, if chosen, i.e., ```verified = True```.
  * ```runtest_tool.run_grader(...)```: a testing manager to have every problem tested as specified in the directive
    * It is like a **student agent** taking care of each student's submission. It reads the directive file (```ans.cfg```), builds ```Grading_Table```, goes through each problem (i.e., for each test case, runs student's python code, gets student's output, asks grader for scores, and combines test-case scores for the problem), reports scores of all problems
      * It was originally designed for python, then the entire suite was extended to handle C/C++. Thus, the run testing may be re-located to the external policy.
  * ```graders.grading```: a grading judge
    * It compares student's output to the reference and grade the output according to the specified policy.
    * Regular policies, ```exact``` (full score or nothing), ```parline``` (partial credit by line), and ```numtol2``` (partial credit by line with numerical tokens evaluated on tolerance), should work fine for general cases.
    * The policy ```external``` allows the entire process of run testing and grading to be passed on to the specified external policy, which can arbitrarily added. The ```graders.grading``` simply passes everything (necessary) to the external file through running arguments along with problem score and reporting mode. 

Issues
  * Clearly, ```graders.grading``` does very little: it just relays task to the real grading policy. (I can get rid of ```graders.grading``` and move the relaying into ```runtest_tool.run_grader```.)
    * If policy is external, it takes an unnecessary route: ```runtest_tool.run_grader``` -->  ```graders.grading``` --> the external script
    * It seems simpler just to have ```python3.5 extpolicy3.py ./cfg/ext2P9.cfg``` in the place of ```ans.cfg```'s Run and ```360``` in the place of Runtime. To accompany this, a new grading policy may forward the runtest output, which now is from extpolicy rather than student's code, to the score.
  * If I have students submit their answers by tar, it should work. But, it is a little bit awkward. It may be nicer to have it in an embeded html, where a student can put his/her code directly on the web.
    * This raises another issue. Autolab embedded form gives out student's answer in a json text file. This json file has all answers. It is not like tar, which contains each file for each problem. This is one file has contents of every questions.
      * Option 1: forget efficiency. Put this one file to each iteration of ```runtest_tool.run_grader```
        * It may be ugly, but it will work and does not require much on fixing the code.
      * Option 2: have a dedicated code for embeded form, like [Autolab course 811100-s19's Mocking Test](https://autolab.en.kku.ac.th/courses/811100-s19/assessments/testembeddedform)
      * Option 3: re-design the pipeline
        * Perhaps, I can handle this cleanly in ```grader_center4``` (or maybe not?)

# Feb 26th, 2021. (dev/2021e)
For LCA class (option: Grader = ```numtol2``` in ```ans.cfg```)
  * better handling a negative sign, i.e., ```- ###``` vs ```-###``` 
  * better reveal wrong format without giving out the correct calculation

Changes
  * ```graders.py``` (add ```numtol2``` option; have ```policy == 'external'``` accommodate other reporting modes (```!= 'Deploy'```)
  * ```policy2021.py``` (new file, implementing ```numtol2```, i.e., ```numtol_policy2``` function)

Examples
  * Given ref: ```-18 V```, both student's answer: ```-18 V``` and ```- 18 V``` are correct.
  * Incorrect answer will see the feedback marking the incorrect spot without revealing the calculation (i.e., number)
    * ref: ```v1 = -18 V```
      * student's answer: ```v1 = 18 V```(Wrong answer) will see
      ```
      v1 = 18 V
      _____##
      ```

      * student's answer: ```v = -18 V```(Right answer, incorrect format) will see
      ```
      v = -18 V
      # 
      ```
      * student's answer: ```v = -18```(Right answer, missing unit) will see
      ```
      v = -18 
      _______# 
      ```

  * Given ref: ```18 V```, both student's answer: ```-18 V``` and ```- 18 V``` are incorrect.
    * ref: ```v1 = 18 V```
      * student's answer: ```v1 = - 18 V```(Wrong answer) will see
      ```
      v1 = -18 V
      _____###
      ```

Download [tar](https://github.com/tatpongkatanyukul/Autolab/blob/main/dev/autogradeHidNum.tar)
See [Test numtol2](https://autolab.en.kku.ac.th/courses/Test/assessments/numtol2), [EN001203-s20 A000](https://autolab.en.kku.ac.th/courses/001203-s20/assessments/a000)


# Feb 17th, 2021
For CPG class
  * better ```Test``` reporting mode of ```numtol```
    * That is having a marker indicating where the first difference is found

Changes
  * ```base_policies.py``` and ```numgraders.py```

Examples
  * Different alphabet (Wrong calculation)
```
numtol_policy: * reference : Enter 2 integers: z = 0.5625
numtol_policy: * student   : Enter 2 integers: z = 0
numtol_policy: * difference: ______________________#
```
  * Different token (Wrong logic)
```
numtol_policy: * reference : Height: Cannot play
numtol_policy: * student   : Height: Can not play
numtol_policy: * difference: ________###
```

  * Different alphabet (Off format)
```
numtol_policy: * reference : Tmp: Doctor!
numtol_policy: * student   : Tmp: Doctor
numtol_policy: * difference: ___________#
```

See [CPG 2021 MTE](https://autolab.en.kku.ac.th/courses/001203-s20/assessments/e1)
