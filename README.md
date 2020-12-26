# Autolab

[Autolab @ CoE](http://autolab.en.kku.ac.th/)

## Autograding

Logic flow
  * autograde-Makefile -> submission/driver.sh
  * @ Submission: driver.sh -> Makefile, grader_center.py
  * grader_center.py
    * ```directive```: a filename associating **Student**-submitted Px to **Run** code, to **Grader** code (e.g., ```grading_policy1.py```) to test-case answers.
    * ```P['test']```: code to evaluate, e.g., **Student**'s Px.py or **Run** code. 
      * in ***```subprocess.run([python_command], P['test'], ...)```***
    * ```P['grader']```: **Grader** code to map from **Student**'s answers and test-case answers to scores. 
      * in ```subprocess.run([python_command], P['grader'], ...)```
    * ```python_command = 'python3.5'```
