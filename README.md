# Autolab

[Autolab @ CoE](http://autolab.en.kku.ac.th/)

## Autograding

Logic flow
  * autograde-Makefile -> submission/driver.sh
  * @ Submission: driver.sh -> Makefile, grader_center.py
  * grader_center.py -> ```subprocess.run([python_command], P['grader'], ...)```
