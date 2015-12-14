import sys
import pickle
import os.path

from interpreter import PyCalcInterpreter

intro = '''PyCalc -- Python Calculator
Type "help" for help. Type "quit" to quit.'''

prompt = '>>> '

help_str = '''Enter arithmetic expressions at the prompt.

Special commands:
    quit
        Exit the program.
    vars
        View the stored variables.
    del (pattern)*
        Delete all variables matching one of the given patterns.
        If no pattern is specified, delete all variables.
    help
        View this help message.'''

var_fname = '.pycalcvars'
variables = {}
if os.path.isfile(var_fname):
    with open(var_fname, 'rb') as file:
        variables = pickle.load(file)

pycalc = PyCalcInterpreter(intro, prompt, help_str, variables)

if len(sys.argv) > 1:
    # If there are command-line arguments, treat them as an expression and
    # try to evaluate it.
    pycalc.onecmd(' '.join(sys.argv[1:]))
else:
    # Otherwise, enter interactive mode.
    pycalc.cmdloop()

with open(var_fname, 'wb') as file:
    pickle.dump(variables, file)
