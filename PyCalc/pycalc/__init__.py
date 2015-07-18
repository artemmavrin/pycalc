from math import e, pi
from re import compile

from pycalc.lang import is_variable
from pycalc.lang.parser import Parser, ParseException
from pycalc.misc import print_iterable, print_table, underline_substring
from itertools import chain

constants = {'e': e, 'pi': pi}


class PyCalc(object):

    def __init__(self,
                 prompt='>>> ',
                 quit_command='quit',
                 vars_command='vars',
                 help_command='help',
                 delete_command='del',
                 comment='#',
                 ):
        self.variables = {}
        self.prompt = prompt
        self.quit = quit_command
        self.vars = vars_command
        self.help = help_command
        self.delete = delete_command
        illegal_vars = [self.quit, self.vars, self.help, self.delete]
        self.parser = Parser(illegal_vars=illegal_vars)
        self.comment = comment

    def compute(self, line):
        self.parser.parse(line)
        self.names = self.parser.names
        tree = self.parser.tree
        if tree.set_variables(self.variables) or tree.set_variables(constants):
            self.value = tree.evaluate()
            for name in self.names:
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
        print('Example:')
        print(self.prompt + '1 + 2')
        print('ans =')
        print('    3')
        print(self.prompt + 'a = pi')
        print('a =')
        print('    ' + str(pi))
        print(self.prompt + 'a + e')
        print('ans =')
        print('    ' + str(pi + e))
        print(self.prompt + 'b = c = 10')
        print('b, c =')
        print('    10')
        print(self.prompt + 'log|1-2| # this is a comment')
        print('ans =')
        print('    0.0')
        print()
        print('Special commands:')
        print(indent + self.quit)
        print(2 * indent + 'Exit the program.')
        print(indent + self.vars)
        print(2 * indent + 'View the stored variables.')
        print(indent + self.delete + ' (pattern)*')
        print(2 * indent + 'Delete all variables matching one of the given ' +
              'patterns.')
        print(2 * indent + 'If no patterns are specified, all variables are ' +
              'deleted.')
        print(indent + self.help)
        print(2 * indent + 'View this help message')

    def delete_variables(self, line):
        if self.variables:
            tokens = line.split()
            if len(tokens) == 1:
                self.variables.clear()
                print('Deleted all variables.')
            else:
                names = sorted(self.variables.keys(), key=lambda s: s.lower())
                deleted = []
                failed_patterns = []
                patterns = tokens[1:]
                for pattern in tokens[1:]:
                    regex = compile('^' + pattern + '$')
                    match_found = False
                    for name in names:
                        if regex.match(name) and name in self.variables:
                            match_found = True
                            del self.variables[name]
                            deleted.append(name)
                    if not match_found:
                        failed_patterns.append(pattern)
                if deleted:
                    print_iterable(chain(['Delteted:'], deleted))
                    if failed_patterns:
                        print('No variables matched the following pattern' +
                              int(bool(failed_patterns[1:])) * 's' + ':')
                        print_iterable(failed_patterns)
                else:
                    print('No variables matched the given pattern' +
                          int(bool(patterns[1:])) * 's' + '.')
        else:
            print('There are no variables to delete.')

    def __call__(self):
        print('PyCalc -- Python PyCalc')
        print("Type '" + self.help + "' for help.")

        while True:
            line = input(self.prompt)
            # remove comments
            line = line.split(self.comment)[0].strip()
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
                    underline_substring(ex.expression, ex.start, ex.end)
                except Exception as ex:
                    print('Runtime error:', str(ex))
                else:
                    print_iterable(self.names, sep=', ', end=' =\n')
                    print('    ' + str(self.value))
