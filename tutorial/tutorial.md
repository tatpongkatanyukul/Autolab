# Tutorial

---

## Example

Questions or Problems
  * Question is meant for something student answered in a text file
  * Problem is meant for a program to be submitted
  
### Autograder

Grading configuration file (```ans.txt```):
![Write the ans.txt](https://github.com/tatpongkatanyukul/Autolab/blob/main/tutorial/anstxt.png)

The ```ans.txt``` specifies:
  * every problem and question
  * each line describing each problem
    * The first line is a header. Autograder does not read it, but it's good to have it there as a reference.
  * each field in every line is separated by ```\;```
  * Fields are arranged in order
    * Px: problem or question id, e.g., Q1, Q2, P3
    * Points: full score for the problem
    * Student: a submitted filename to which student has to comply 
    * Run: a command to run to get a result; this allows flexible type of submission, e.g., text, cpp, py
    * Runtime: a maximal runtime allowed in second
    * Grader: 
    * GAttrib:
    * Report:
    * Test Case: in ans, in ans, in ans 
