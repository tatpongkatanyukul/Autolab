# Walk-Along Tutorial

Summarized steps
* 1. Write questions/problems
  * [Handout example](https://github.com/tatpongkatanyukul/Autolab/blob/main/handout.pdf)
* 2. Prepare the answers/reference outputs
  * Put each of them in answer files, e.g., ```Q1.ans```, ```P5c1.in```, ```P5c1.ans```
* 3. Write the grading configuration ```ans.txt```
* 4. Set the grader center (GC), i.e., ```grader_center4.py``` for Autolab
  * ```MODE='Autolab'```
  * set ```verified = True``` for identity verification session, e.g., exam (or mocking one), otherwise ```verified = False```
* 5. Pack all the autograder facilities
  * ***Make sure that the student folder is empty.***
* 6. Build and configure assessment
* 7. Upload the packed tar file along with the ```Makefile``` into autograder
* 8. Test submission

---

## 1.

## 2.

## 3.

## 4.


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

