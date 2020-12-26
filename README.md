# Autolab

[Autolab @ CoE](http://autolab.en.kku.ac.th/)

## Autograding

Logic flow
  * autograde-Makefile -> submission/driver.sh
  * @ Submission: driver.sh -> Makefile, grader_center.py
  * grader_center.py
    * ```directive```: a filename associating **Student**-submitted Px to **Run** code, to **Grader** code (e.g., ```grading_policy1.py```) to test-case answers.
    * ```P['test']```: code to evaluate, e.g., **Student**'s Px.py or **Run** code. In ```subprocess.run([python_command, P['test']],...)```
    * ```P['grader']``` in ```subprocess.run([python_command], P['grader'], ...)```
    * ```python_command = 'python3.5'```
