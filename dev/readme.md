# Apr 17th, 2021. (dev/2021g)
Key (intended) additions
  * fix ```json_handler``` and its associcated codes, so that ```python dispatcher.py -autolab -json``` and ```python dispatcher.py -autolab -json -verified``` work
  * add personalized grading policy, i.e., given a student's email (obtained from ```settings.json```), grader selects an associated reference text to compare against.
    * this allows a personalized exercise, where a student gets one's own questions different from other students and one's answers are graded accordingly.
  * add personalized post message feature, i.e., after grading student's submission, a grader give out a personalized message along with scores and other comments.
    * this personalized post message feature can be exploited as a primitive question delivery, where a post message could be a next question information

# Apr 16th, 2021. (dev/2021f)

**WARNING!** ```json_handler``` (option ```-json```) has not been tested yet
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
