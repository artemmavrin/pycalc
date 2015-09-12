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

PyCalcInterpreter(intro, prompt, help_str).cmdloop()
