# Debug the Grading

Flow
  * ```grader_center4.py``` -> ```runtest_tool.py```
  
Procedure
  * Put test submission into the ```student``` folder
  * Run ```runtest_tool.py```
  * Focus on ```run_grader``` function
    * ```ans``` is a reference text
    * ```rout``` is a submission output
  * If both ```ans``` and ```rout``` look alike, check ```graders.py```
    * It may be trifle: miss a character, typo or white space issues. (Sometimes, unseen character comes up.)
    * Write contents of ```ans``` and ```rout``` to files and open them with notepad++ with showing all characters to see the hidden characters.
  * ```\r``` and ```\n``` are often the causes. 

```graders.py```
```Python
       :
    # Check file in notepad++ with [view] > [show symbol] > [show all characcters]
    f = open('debug' + Px + 'out.txt', 'w')
    f.write(test_out)
    
    f = open('debug' + Px + 'gt.txt', 'w')
    f.write(gt_ans)
       :
```
