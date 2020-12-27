# Walk-Along Tutorial

## Pack all the autograder facilities

***Make sure that the student folder is empty.***
Failure to do so would have given some students a free ride: a prior submission has files he/she did not submit.

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

