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
  * every problem and question,
  * each line describing each problem,
    * The first line is a header. Autograder does not read it, but it's good to have it there as a reference.
  * each field in every line by ```\;``` delimiter.
  * Fields are arranged in order.
    * Px: problem or question id, e.g., Q1, Q2, P3
    * Points: full score for the problem
    * Student: a submitted filename to which student has to comply 
    * Run: a command to run to get a result; this allows flexible type of submission, e.g., text, cpp, py
    * Runtime: a maximal runtime allowed in second
    * Grader: a grader policy, i.e., exact, parline, numtol
      * exact: submission matching reference exactly gets full score, otherwise 0. See Q1 (on ```ans.txt```) for example.
      * parline: partial credit by a number of lines matched to reference lines. Each line must match exactly.
      * numtol: partial credit by a number of lines matched to reference lines. 
        * Each line must comply to a designated format and numeric answer can be tolerated with the specified tolerance (through ```GAttrib```)
    * GAttrib: attributes for grader, e.g., when using ```numtol```, GAttrib specifies tolerance. See Q3 on the ```ans.txt``` image.
    * Report: Grader's reporting mode
      * ```Test```: reports details, inc. submission output and reference answer. See Q2, Q3, P5, and P6 for examples
      * ```Deploy```: only reports scores.
    * Test Case: test-case input and reference output files in pair, each pair is delimited by ```,```. There can be as many test cases as please. See P5 for example.
