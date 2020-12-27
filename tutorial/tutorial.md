# Tutorial

---

### Naming Convention

Questions or Problems
  * Question is meant for something student answered in a text file, e.g., Q1, Q2, and Q3.
  * Problem is meant for a program to be submitted, e.g., P4, P5, and P6.
  
### Autograder


#### Having the right strategy is the key

Autograder works on the output that a test subject gives out to the standard output, e.g., screen.
Therefore, it requires a proper strategy to have it work as it should
  * Testing function, class, or any kind of module should be tested through the ``auxiliary file''.
    * E.g., instead of running student's ```P1.py```, have ```P1_aux.py``` to call a function under test and check out the output ```P1_aux.py``` produces.
  * Similearly, testing operation on files should be tested through the ``auxiliary file''.
    * E.g., instead of running student's ```P2.py```, have ```P2_aux.py``` to call ```P2.py``` and then read the file, which as supposed to be prepared by ```P2.py``` and print it out. Check out the output ```P2_aux.py``` produces.

Our autograder is flexible such that it can take a submission (and check if it is there), but run another file to test it. See ```ans.txt``` section for details.


#### ```ans.txt```
Grading configuration file (```ans.txt```):
![Write the ans.txt](https://github.com/tatpongkatanyukul/Autolab/blob/main/tutorial/anstxt.png)

The ```ans.txt``` specifies:
  * every problem and question,
  * each line describing each problem,
    * The first line is a header. Autograder does not read it, but it's good to have it there as a reference.
  * each field in every line by ```\;``` delimiter.
  * Fields are arranged in order.
    * Px: problem or question id, e.g., Q1, Q2, P3
    * Points: full score for the problem
    * Student: a submitted filename to which student has to comply 
    * Run: a command to run to get a result; 
      * This allows flexible type of submission, e.g., text, cpp, py.
      * It may seem dangerous. But, recall that ```python P1.py``` (for python) versus ```g++ P1.cpp -o P1.exe; ./P1.exe``` (for C++) versus ```Q_aux1.exe P1.txt``` (for text answer).
        * Check out older version (e.g., ```mm_grader_center.py```, ```grader_center2.py```), if uncomfortable with this.
        
      * _!CAUTION!_ Command inconsistency between local machine and autolab server.
        * E.g., ```py35_image``` uses ```python3.5 P1.py```. Also, ```Q_aux1.exe``` compiled on Windows does not work on Unix.
    * Runtime: a maximal runtime allowed in second
    * Grader: a grader policy, i.e., exact, parline, numtol
      * exact: submission matching reference exactly gets full score, otherwise 0. See Q1 (on ```ans.txt```) for example.
      * parline: partial credit by a number of lines matched to reference lines. Each line must match exactly.
        * recommended option (as Dec 27th, 2020)
      * numtol: partial credit by a number of lines matched to reference lines. 
        * Each line must comply to a designated format and numeric answer can be tolerated with the specified tolerance (through ```GAttrib```)
        * _!CAUTION!_ ```numtol``` is too rough. See to-do list.
    * GAttrib: attributes for grader, e.g., when using ```numtol```, GAttrib specifies tolerance. See Q3 on the ```ans.txt``` image.
    * Report: Grader's reporting mode
      * ```Test```: reports details, inc. submission output and reference answer. See Q2, Q3, P5, and P6 for examples
      * ```Deploy```: only reports scores.
    * Test Case: test-case input and reference output files in pair, each pair is delimited by ```,```. There can be as many test cases as please. See P5 for example.
      * Each test case needs both input and ans files. For any problem not taking any input, use the ```dummy.in```.
  * ```#``` as the first character in the line indicating the comment-out line. E.g., P7 is commented out. There will be ***no grading*** for P7.
  
#### Grading Policy

Grading Policy is specified in ```ans.txt```.
So far, we have:
  * ```exact```
  * ```parline``` (Best one, so far)
  * ```numtol``` (too rough!!! See to-do list.)
  
A more flexible policy can be addressed through modification of ```graders.py```.
It is advised to add a new policy, rather than modifying a workable existing one.

#### Test-case input file ```Px.in``` or ```Pxcx.in```

Each file has each input text as it would be typed in by a user.

_!CAUTION!_ A ***new line*** is needed to finish the entry.
Multiple entries are also possible.

Example ```P5c1.in```:
```
Kubo

```

#### Test-case reference output file ```Px.ans``` or ```Pxcx.ans```

Each file has reference output text in its final stage (if it's meant for a program taking multiple inputs).

Example ```P5c1.ans```:
```
Name: Kubo
Hello, Kubo.
```

**PS.** GC (through ```graders.py```) has prepared for discrepancy between Unix and Windows, such as a new line: ```\r```, ```\r\n```, ```\n```. But, it is always safe to double check.

#### Running mode

  * ```MODE='Test'```: this sets the grader center (GC) to do a single test on whatever in ```./student``` folder.
    * It is a convenient way to test autograder, before deployment.
    * It also comes in handy, when debugging the unexpected.
  * ```MODE='Autolab'```: this sets GC ready for autolab.
    * _!CAUTION!_ Don't forget to test submission through the Autolab system. There may be some discrepancy, e.g., windows vs unix, dependency or other issues.
  * MODE='Local Batch': this sets GC to perform batch grading on a local computer. This mode is very handy, when Autolab server fails.
  * _!CAUTION!_ Without Autolab and docker facilities, this mode is risky for our own computer. ***Better to set it up and run on a computer that does not have any important data too value to loose.***
  
#### Identity Verification

  * ```verified = True``` puts GC into the verification mode. When student identity cannot be verified, GC refuses to grade.
    * It is intended for the exam.
    * It needs 
      * ```codebook.txt``` tying e-mail, student id, and verification code together. 
        * This has be prepared in the autograd tar pack.
      * ```settings.json``` providing student id of the submission according to the log-in. 
        * Autolab (as Ajahn Wasu has tweaked it) provides this.
      * ```verify.txt``` providing student id and the verification code.
        * student has to put this file along with other submission files.
    * _!CAUTION!_ Don't forget to arrange a mocking exam, so that students are familiar with it, before going for the real one.
  * ```verified = False``` renders GC into a regular mode. No verification is required.
  

## To-Do List

  * Add case-sensitive/case-insensitive option for ```exact``` and ```parline``` grader policies.
  * Docker image w/ ```python``` rather than ```python3.5```
  * Docker images for other courses, e.g., LCA (w/ SPICE), ANN (w/ numpy), Pattern Recognition (PR w/ numpy, cv2, pytorch)
  * Add hint comments to grader policies, e.g., ```exact``` and ```parline``` with ```GAttrib: hint=P7.hnt```
    * After grading, if student did not get full score, show content in the hint file.
  * ```numgraders.py``` is too rough. It is rigid and hard to use. It should be fixed! But, I need time, starting from decision of its capabilities, e.g., ```3.45```, ```4mA```, ```3+j5V```, ```(Q3.1) 8.2```.
