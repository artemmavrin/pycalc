from math import e, pi
from re import compile

from pycalc.lang import is_variable
from pycalc.lang.parser import Parser, ParseException
from pycalc.lang.tokenizer import underline_token
from pycalc.misc import print_iterable, print_table

default_variable = 'ans'

constants = {'e': e, 'pi': pi}


class Calculator(object):

    def __init__(self,
                 prompt='>>> ',
                 quit_command='quit',
                 vars_command='vars',
                 help_command='help',
                 delete_command='del'
                 ):
        self.variables = {}
        self.prompt = prompt
        self.quit = quit_command
        self.vars = vars_command
        self.help = help_command
        self.delete = delete_command
        self.illegal_vars = [self.quit, self.vars, self.help, self.delete]
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
            var_table = [['name', 'value', 'type']]
            for name in sorted(self.variables.keys(), key=lambda s: s.lower()):
                value = self.variables[name]
                var_table.append([name, value, type(value).__name__])
            print_table(var_table)

    def show_help(self):
        indent = '  '
        print('Enter arithmetic expressions or variable assignments '
              'at the prompt.')
        print()
        print('Special commands:')
        print(self.quit)
        print(indent + 'Exit the program.')
        print(self.vars)
        print(indent + 'View the stored variables.')
        print(self.delete + ' (pattern)*')
        print(indent + 'Delete all variables matching one of the given ' +
              'patterns.')
        print(indent + 'If no patterns are specified, all variables are ' +
              'deleted.')
        print(self.help)
        print(indent + 'View this help message')

    def delete_variables(self, line):
        if self.variables:
            tokens = line.split()
            if len(tokens) == 1:
                self.variables.clear()
                print('Deleted all variables.')
            else:
                names = sorted(self.variables.keys(), key=lambda s: s.lower())
                deleted = []
                for pattern in tokens[1:]:
                    regex = compile(pattern)
                    for name in names:
                        if regex.match(name) and name in self.variables:
                            del self.variables[name]
                            deleted.append(name)
                if deleted:
                    print('The following variables were deleted:')
                    print_iterable(deleted)
                    print()
                else:
                    print('No variables matched the given patterns.')
        else:
            print('There are no variables to delete.')

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
            elif line.startswith(self.delete):
                self.delete_variables(line)
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
