# Autolab

[Autolab @ CoE](http://autolab.en.kku.ac.th/)

## Process
  * student.tar (student's submission)
  * Makefile (script starting grader; name may appear different) 
  * autograde.tar (grading tools; name may appear different)
    * extracted to: submission


## Autograding

Logic flow
  * autograde-Makefile -> submission/driver.sh
  * @ submission: driver.sh -> Makefile, mm_grader_center.py
  * mm_grader_center.py
    * ```directive```: a filename associating **Student**-submitted Px to **Run** code, to **Grader** code (e.g., ```grading_policy1.py```) to test-case answers.
    * ```P['test']```: code to evaluate, e.g., **Student**'s Px.py or **Run** code. 
      * in ***```subprocess.run([python_command, P['test']], ...)```***
    * ```P['grader']```: **Grader** code to map from **Student**'s answers and test-case answers to scores. 
      * in ```subprocess.run([python_command, P['grader']], ...)```
    * ```python_command = 'python3.5'```


## Migrating to C++

  * (1) ```mm_grader_center.py``` is modified to ```grader_center2.py```
  * (2) Key is at ```run_grader(...)```:
    * Only ***```subprocess.run([python_command], P['test'], ...)```*** has to be changed.
    * To seamlessly integrate it, I can use compound command, e.g., ```g++ aloha.cpp -o testrun.exe; ./testrun.exe```
      * **```subprocess.run([runtest_command, P['runtest'], runtest_suffix], ...)```**
      * ```runtest_command = "g++"```
      * ```runtest_suffix = "-o runtest.exe; ./runtest.exe"```


## Grading Policies

  * (1) No partial credit
  * (2) partial credit
  * (3) numerical tolerance (see LCA autolab)
  
  
## Tuturial
  * [Autolab how to create an exercise (aka assessment)](https://github.com/tatpongkatanyukul/Autolab/blob/main/tutorial/build_assessment.md)
  * [Autograder](https://github.com/tatpongkatanyukul/Autolab/blob/main/tutorial/tutorial.md)
  * [Autolab tutorial](https://github.com/tatpongkatanyukul/Autolab/blob/main/tutorial/readme.md)


## To-Do List
  * (1) Have Pre-problem run script. So that, C++ can be compiled only once.
  * (2) Have Post-problem run script. So that, all p.exe gets cleaned up.
  * (3) Have a grading policy with hint
