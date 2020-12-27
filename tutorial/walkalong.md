# Walk-Along Tutorial

Summarized steps
* 1. Write questions/problems
  * [Handout example](https://github.com/tatpongkatanyukul/Autolab/blob/main/handout.pdf)
* 2. Prepare the answers/reference outputs
  * Put each of them in answer files, e.g., ```Q1.ans```, ```P5c1.in```, ```P5c1.ans```
* 3. Write the grading configuration ```ans.txt```
* 4. Test the grader center (GC) and make sure that grader work reliably
* 5. Set the GC, i.e., edit ```grader_center4.py``` 
  * ```MODE='Autolab'``` for running on Autolab
  * set ```verified = True``` for identity verification session, e.g., exam (or mocking one), otherwise ```verified = False```
* 6. Pack all the autograder facilities
  * ***Make sure that the student folder is empty.***
* 7. Build and configure assessment
* 8. Upload the packed tar file along with the ```Makefile``` into autograder
* 9. Test submission

---

## 1. Write questions/problems

Questions or problems should be written with autograding (and its limitations) in mind.
Have a good strategy on asking questions or posing problems. So that the answer or the output can be verified effectively.

## 2. Prepare the answers/reference outputs

Example of the content of the input file
```
Kubo

```

Example of the content of the output file
```
Name: Hello, Kubo.

```

Notice that the reference output does not contain whatever a user types in (incluing a new line).

The best reference output can be obtained by taking the real output from a correct program solving the the underlying problem. Run it. Capture the output. Separate what a user types in from what a program prints out.


## 3. Write the grading configuration ```ans.txt```

Example of the ```ans.txt```
![ans.txt](https://github.com/tatpongkatanyukul/Autolab/blob/main/tutorial/anstxt.png)

See [field meanings](https://github.com/tatpongkatanyukul/Autolab/blob/main/tutorial/tutorial.md#anstxt).

## 4. Test the GC

Test run GC on a mocking submission.
  * 1. Put mocking submitted answers and programs in the ```student``` folder
  * 2. Run GC in ```Test``` mode
  * 3. Examine the outcomes

Put mocking submission in the ```student``` folder
![working student folder](https://github.com/tatpongkatanyukul/Autolab/blob/main/tutorial/workable_student_fold.png)

Example of the final outcome
```
{"scores": {"Q1": 5, "Q2": 5, "Q3": 8, "P4": 10, "P5": 20, "P6": 0, "P8": 10},"scoreboard":[5, 5, 8, 10, 20, 0, 10, 58]}
```

It is important to try a wrong answer as well as imperfect program and missing submission to test the grader.
The above example has Q1, Q2, P4, P5 and P8 the perfect scores, but Q3 gets partial credits and P6 is missing.

## 5. Edit the GC

Once we have confidence with the grader integrity, we have to prepare it for the autolab server. 

Edit the GC to have ```MODE = 'Autolab'``` as shown below.

```grader_center4.py```
```Python
:
    MODE = 'Autolab'      # to deploy on Autolab server
    # MODE = 'Test'           # to test a single submission
    # MODE = 'Local Batch'  # to evaluate students' submission, when autolab fails

    # verified = True # for exam/mocking exam
    verified = False # for exercises/homework
:
```

Also, make sure that all discrepancies between the local machine and Autolab server have been properly handled.
For example, docker image ```py35_image``` refers to ```python3.5``` for python interpreter. Therefore, if using this ```py35_image```, all calls to ```python``` have to be changed properly.
![anstxt for py35_image](https://github.com/tatpongkatanyukul/Autolab/blob/main/tutorial/anstxt_autolab.png)


## 6. Pack all the autograder facilities

***Make sure that the student folder is empty.*** Failure to do so would have given some students a free ride: a prior submission has files he/she did not submit.

![Fresh student folder](https://github.com/tatpongkatanyukul/Autolab/blob/main/tutorial/fresh_student_folder.png)

Local Batch Model takes care of cleaning the student folder. It is safe in the local batch mode.
```grader_center4.py```
```Python
          :

    elif MODE == 'Local Batch':
          :

            # Clean the target folder
            clean_folder(untar_dir, confirm=False)
                      :
```

Pack the autograder
![Pack the autograder](https://github.com/tatpongkatanyukul/Autolab/blob/main/tutorial/pack_autograder.png)

## 7. Build and configure assessment


## 8. Upload the packed tar file along with the ```Makefile``` into autograder


## 9. Test submission
