from math import e, pi
from pycalc.lang import is_variable
from pycalc.lang.parser import Parser, ParseException
from pycalc.lang.tokenizer import underline_token
from pycalc.misc import print_table

default_variable = 'ans'

constants = {'e': e, 'pi': pi}


class Calculator(object):

    def __init__(self,
                 prompt='>>> ',
                 quit_command='quit',
                 vars_command='vars',
                 help_command='help',
                 ):
        self.variables = {}
        self.prompt = prompt
        self.quit = quit_command
        self.vars = vars_command
        self.help = help_command
        self.illegal_vars = [self.quit, self.vars, self.help]
        self.parser = Parser(self.illegal_vars)

    def compute(self, line):
        line = line.strip()

        *names, expression = line.split('=')
        names = list((name.strip() for name in names))
        if not names:
            names = [default_variable]

        # check that all variable names are valid
        for name in names:
            if not is_variable(name) or name in self.illegal_vars:
                raise Exception('Illegal assignment: ' + name +
                                ' is not a valid variable name')
        self.parser.parse(expression)
        tree = self.parser.tree
        if tree.set_variables(self.variables) or tree.set_variables(constants):
            self.value = tree.evaluate()
            for name in names:
                self.variables[name] = self.value
        else:
            raise Exception('Encountered unknown variable.')

    def print_variables(self):
        if not self.variables:
            print('No variables to show.')
        else:
            var_table = [['NAME', 'VALUE']]
            for name in sorted(self.variables.keys()):
                var_table.append([name, self.variables[name]])
            print_table(var_table)

    def show_help(self):
        print('Enter arithmetic expressions or variable assignments '
              'at the prompt.')
        print()
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
