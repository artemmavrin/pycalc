from math import e, pi
from lang import is_variable
from lang.parser import Parser, ParseException
from lang.tokenizer import underline_token

default_variable = 'ans'

constants = {'e': e, 'pi': pi}


class Calculator(object):

    def __init__(self,
                 prompt='>>> ',
                 quit_command='quit',
                 vars_command='vars',
                 help_command='help'):
        self.variables = {}
        self.parser = Parser()
        self.prompt = prompt
        self.quit = quit_command
        self.vars = vars_command
        self.help = help_command

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
        if tree.set_variables(self.variables) or tree.set_variables(constants):
            self.value = tree.evaluate()
            self.variables[name] = self.value
        else:
            raise Exception('Encountered unknown variable.')

    def print_variables(self):
        if not self.variables:
            print('No variables to show.')
        else:
            names = sorted(self.variables.keys())
            name = 'NAME'
            value = 'VALUE'
            name_length = max(len(name), max(len(name) for name in names))
            print(name + (name_length - len(name)) * ' ' + ' ' + value)
            for name in names:
                value = str(self.variables[name])
                print(name + (name_length - len(name)) * ' ' + ' ' + value)

    def show_help(self):
        print('Special commands:')
        print(self.quit + ': exit the program')
        print(self.vars + ': view the stored variables')
        print(self.help + ': view this help message')

    def __call__(self):
        print('PyCalc -- Python Calculator')
        print("Type '" + self.help + "' for help.")

        while True:
            line = input(self.prompt)
            if line == self.quit:
                break
            elif line == self.vars:
                self.print_variables()
            elif line == self.help:
                self.show_help()
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
