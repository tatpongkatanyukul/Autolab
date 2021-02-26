
# Feb 26th, 2021.
For LCA class (option: Grader = ```numtol2``` in ```ans.cfg```)
  * better handling a negative sign, i.e., ```- ###``` vs ```-###``` 
  * better reveal wrong format without giving out the correct calculation

Changes
  * ```graders.py``` (add ```numtol2``` option)
  * ```policy2021.py``` (new file, implementing ```numtol2```, i.e., ```numtol_policy2``` function)

Examples
  * Given ref: ```-18 V```, both student's answer: ```-18 V``` and ```- 18 V``` are correct.
  * Incorrect answer will see the feedback marking the incorrect spot without revealing the calculation (i.e., number)
    * ref: ```v1 = -18 V```
      * student's answer: ```v1 = 18 V```(Wrong answer) will see
      ```
      v1 = 18 V
      _____##
      ```

      * student's answer: ```v = -18 V```(Right answer, incorrect format) will see
      ```
      v = -18 V
      # 
      ```
      * student's answer: ```v = -18```(Right answer, missing unit) will see
      ```
      v = -18 
      _______# 
      ```

  * Given ref: ```18 V```, both student's answer: ```-18 V``` and ```- 18 V``` are incorrect.
    * ref: ```v1 = 18 V```
      * student's answer: ```v1 = - 18 V```(Wrong answer) will see
      ```
      v1 = -18 V
      _____###
      ```

Download [tar](https://github.com/tatpongkatanyukul/Autolab/raw/main/dev/autograde210226a.tar)
See [test](https://autolab.en.kku.ac.th/courses/Test/assessments/numtol2)
