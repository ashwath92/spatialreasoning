Execution Details:

The code is entirely in Python 3, so it has to be executed with a Python 3 interpreter. It will not work with Python 2.x.

Classical spatial reasoning model (Johnson-Laird and Byrne):
To execute the Python code for the classical spatial reasoning model (Johnson-Laird and Byrne), one of the following commands is executed based on the operating system: 
Linux/Mac: python3 spatial_reasoning.py problem_type problem_no.
Windows (assuming only Python 3.x is installed): python spatial_reasoning.py problem_type problem_no.
where
problem_type is one of {combination, deductive, indeterminate, inconsistent, genertedet, generateindet}
problem_no is the problem number under the given problem type. 

Prism Model:
To execute the  Python code for the  Prism model, one of the following commands is executed based on the operating system:
Linux/Mac: python3 prism.py problem_type problem_no.
Windows (assuming only Python 3.x is installed): python prism.py problem_type problem_no.
where
problem_type is one of {combination, deductive, indeterminate, inconsistent, genertedet, generateindet, generateall}
problem_no is the problem number under the given problem type.


Example:

To execute deductive 9 using Spatial reasoning, run:

Linux/Mac: python3 spatial_reasoning.py deductive 9
Windows: python spatial_reasoning.py deductive 9

To execute the same problem, deductive 9, using Prism, run:

Linux/Mac: python3 prism.py deductive 9
Windows: python prism.py deductive 9

Other problems are executed in exactly the same way, using the different problem types and numbers.

It is important to note that generateall problems need to be executed with the Prism program, as Johnson-Laird/Byrne's Lisp framework makes it impossible to get all alternative models

To execute problems from the Prism paper using either of the programs, look at Table 4 of the master project report. This table gives the exact problem type and number to execute for
each of the Prism paper problems. The output is also given in the report for both theories.
Similarly, to execute problems from Experiment 1 of the Prism paper, look at Table 5 of the master project report. These are meant to be executed with prism.py, and not with spatial_reasoning.py.
Table 3 of the Master project report also gives the problem type and number for example problems (in the code) of each type mentioned in Tables 1 and 2. 

Please look at the Master project report for more comprehensive details.
