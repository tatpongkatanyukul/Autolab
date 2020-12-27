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
      * numtol: partial credit by a number of lines matched to reference lines. 
        * Each line must comply to a designated format and numeric answer can be tolerated with the specified tolerance (through ```GAttrib```)
    * GAttrib: attributes for grader, e.g., when using ```numtol```, GAttrib specifies tolerance. See Q3 on the ```ans.txt``` image.
    * Report: Grader's reporting mode
      * ```Test```: reports details, inc. submission output and reference answer. See Q2, Q3, P5, and P6 for examples
      * ```Deploy```: only reports scores.
    * Test Case: test-case input and reference output files in pair, each pair is delimited by ```,```. There can be as many test cases as please. See P5 for example.
      * Each test case needs both input and ans files. For any problem not taking any input, use the ```dummy.in```.


## To Do

  * Add case-sensitive/case-insensitive option for ```exact``` and ```parline``` grader policies.
  * Docker image w/ ```python``` rather than ```python3.5```
  * Docker images for other courses, e.g., LCA (w/ SPICE), ANN (w/ numpy), Pattern Recognition (PR w/ numpy, cv2, pytorch)