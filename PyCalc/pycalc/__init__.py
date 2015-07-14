from math import e, pi
from pycalc.lang.parser import Parser, ParseException
from pycalc.lang import is_variable
from pycalc.lang.tokenizer import underline_token

default_variable = 'ans'
constants = {'e': e, 'pi': pi}


class Calculator(object):
    def __init__(self):
        self.variables = {}
        self.parser = Parser()

    def compute(self, line):
        line = line.strip()
        name = ''
        expression = ''

        lhs_rhs = line.split('=')  # left-hand-side/right-hand-side
        if len(lhs_rhs) > 2:
            raise Exception('Multiple assignments are not allowed')
        elif len(lhs_rhs) == 2:
            lhs = lhs_rhs[0].strip()  # left-hand-side of line
            rhs = lhs_rhs[1].strip()  # right-hand-side of line
            if is_variable(lhs):
                name = lhs
                expression = rhs
            else:
                raise Exception('Invalid variable name: ' + lhs)
        else:
            name = default_variable
            expression = line
        self.parser.parse(expression)
        tree = self.parser.tree
        if tree.set_variables(constants) or tree.set_variables(self.variables):
            self.value = tree.evaluate()
            self.variables[name] = self.value
        else:
            raise Exception('Encountered unknown variable.')

    def __call__(self):
        while True:
            line = input('> ')
            if line == 'quit':
                break
            elif line:
                try:
                    self.compute(line)
                except ParseException as ex:
                    print('Runtime error:', str(ex))
                    underline_token(line, ex.start, ex.end)
                except Exception as ex:
                    print('Runtime error:', str(ex))
                else:
                    print(self.value)
