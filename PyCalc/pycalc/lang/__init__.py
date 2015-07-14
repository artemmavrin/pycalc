import re

reserved_chars = ['=', '+', '-', '*', '/', '^', '(', ')', '|', '!']

functions = ['exp', 'log', 'cos', 'sin', 'tan']

variable_regex = re.compile(r'^[a-zA-Z]\w*$')

def is_function(token):
    return token in functions

def is_variable(token):
    return bool(variable_regex.match(token))

def is_int(token):
    try:
        int(token)
        return True
    except ValueError:
        return False

def is_float(token):
    try:
        float(token)
        return True
    except ValueError:
        return False