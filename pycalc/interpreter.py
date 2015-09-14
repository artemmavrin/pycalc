from cmd import Cmd
from itertools import chain
from math import e, pi
from re import compile

from lang import is_variable
from parser import Parser, ParseException
from misc import print_iterable, print_table, underline_substring


constants = {'e': e, 'pi': pi}


class PyCalcInterpreter(Cmd):
    '''PyCalc command-line intrpreter.'''
    def __init__(self, intro, prompt, help_str):
        super().__init__()
        self.intro = intro
        self.prompt = prompt
        self.help_str = help_str
        self.variables = {}
        illegal_vars = ['del', 'help', 'quit', 'vars']
        default_variable = 'ans'
        self.parser = Parser(illegal_vars, default_variable)
        self.comment = '#'

    def default(self, line):
        '''Evaluate the given expression.'''
        try:
            self.parser.parse(line)
            self.names = self.parser.names
            tree = self.parser.tree
            if tree.set_vars(self.variables) or tree.set_vars(constants):
                self.value = tree.evaluate()
                for name in self.names:
                    self.variables[name] = self.value
            else:
                raise Exception('Encountered unknown variable.')
        except ParseException as ex:
            print('Runtime error:', str(ex))
            underline_substring(ex.expression, ex.start, ex.end)
        except Exception as ex:
            print('Runtime error:', str(ex))
        else:
            print_iterable(self.names, sep=', ', end=' =\n')
            print('    ' + str(self.value))

    def emptyline(self):
        '''Ignore blank lines.'''
        pass

    def do_del(self, line):
        '''Delete variables.'''
        if self.variables:
            patterns = line.split()
            if len(patterns) == 0:
                self.variables.clear()
                print('Deleted all variables.')
            else:
                names = sorted(self.variables.keys(), key=lambda s: s.lower())
                deleted = []
                for pattern in patterns:
                    regex = compile('^' + pattern + '$')
                    for name in names:
                        if regex.match(name) and name in self.variables:
                            del self.variables[name]
                            deleted.append(name)
                if deleted:
                    print_iterable(chain(['Delteted:'], deleted))
                else:
                    print('No variables matched the given pattern' +
                        int(bool(patterns[1:])) * 's' + '.')
        else:
            print('There are no variables to delete.')

    def do_help(self, line):
        '''Show the help message.'''
        if line:
            print('The "help" command does not take any arguments.')
        else:
            print(self.help_str)

    def do_quit(self, line):
        '''Exit the program.'''
        if line:
            print('The "quit" command does not take any arguments.')
        else:
            return True

    def do_vars(self, line):
        '''Display the stored variables.'''
        if line:
            print('The "vars" command does not take any arguments.')
        elif not self.variables:
            print('There are no variables to show.')
        else:
            var_table = [['name', 'value', 'type']]
            for name in sorted(self.variables.keys(), key=lambda s: s.lower()):
                value = self.variables[name]
                var_table.append([name, value, type(value).__name__])
            print_table(var_table)

    def cmdloop(self):
        try:
            super().cmdloop()
        except KeyboardInterrupt:
            self.intro='\nKeyboard Interrupt'
            self.cmdloop()

    def precmd(self, line):
        '''Strip comments from the line.'''
        return line.split(self.comment)[0].strip()
