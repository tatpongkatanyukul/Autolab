# Walk-Along Tutorial

Summarized steps
* 1. Write questions/problems
  * [Handout example](https://github.com/tatpongkatanyukul/Autolab/blob/main/handout.pdf)
* 2. Prepare the answers/reference outputs
  * Put each of them in answer files, e.g., ```Q1.ans```, ```P5c1.in```, ```P5c1.ans```
* 3. Write the grading configuration ```ans.txt```
* 4. Set the grader center (GC), i.e., edit ```grader_center4.py``` 
  * ```MODE='Autolab'``` for running on Autolab
  * set ```verified = True``` for identity verification session, e.g., exam (or mocking one), otherwise ```verified = False```
* 5. Pack all the autograder facilities
  * ***Make sure that the student folder is empty.***
* 6. Build and configure assessment
* 7. Upload the packed tar file along with the ```Makefile``` into autograder
* 8. Test submission

---

## 1. Write questions/problems

Questions or problems should be written with autograding (and its limitations) in mind.
Have a good strategy on asking questions or posing problems. So that the answer or the output can be verified effectively.

## 2. Prepare the answers/reference outputs

## 3. Write the grading configuration ```ans.txt```

## 4. Edit the GC

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


## 5. Pack all the autograder facilities

***Make sure that the student folder is empty.*** Failure to do so would have given some students a free ride: a prior submission has files he/she did not submit.

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

