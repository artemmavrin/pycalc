'''Module containing the class for parsing expressions into ASTs

The grammar for the PyCalc language is as follows:

begin ::= add_or_sub
add_or_sub ::= mul_or_div (('+'|'-') mul_or_div)*
mul_or_div ::= negative (('*'|'/') negative)*
negative ::= exponent | '-' negative
exponent ::= factorial | factorial '^' negative
factorial ::= atom ('!')*
atom ::= function | variable | int_number | float_number | enclosure
enclosure ::= parentheses | absolute_value
parentheses ::= '(' begin ')'
absolute_value ::= '|' begin '|'
function ::= <valid function name> enclosure
variable ::= <valid variable name>
int_number ::= <int>
float_number ::= <float>
'''
from pycalc.lang import is_float, is_function, is_int, is_variable
from pycalc.tokenizer import Tokenizer
from pycalc.tree import BinaryOperation, UnaryFunction, Value, Variable


class ParseException(Exception):
    '''Exceptions raised during parsing'''
    def __init__(self, message, expression, token, start, end):
        self.message = message
        self.expression = expression
        self.token = token
        self.start = start
        self.end = end

    def __str__(self):
        return self.message


class Parser(object):
    def __init__(self, illegal_vars=[], default_variable='ans'):
        self.illegal_vars = illegal_vars
        self.default_variable = default_variable

    def parse(self, line):
        line = line.strip()
        *self.names, self.expression = line.split('=')
        self.expression = self.expression.strip()
        # remove whitespace, remove duplicates, and sort
        self.names = sorted(set((name.strip() for name in self.names)))
        # if no names are specified, use the default variable name
        self.names = [self.default_variable] if not self.names else self.names

        # Check that all variable names are valid
        for name in self.names:
            if not name:
                raise Exception('Illegal assignment: no variable or ' +
                                'expression specified.')
            if not is_variable(name) or name in self.illegal_vars:
                raise Exception('Illegal assignment: ' + name +
                                ' is not a valid variable name')

        # Parse expression according to grammar rules
        self.tokenizer = Tokenizer(self.expression)
        self.tree = self.begin()

        # the tokenizer should be out of tokens
        if self.tokenizer.has_next():
            token, start, end = next(self.tokenizer)
            message = 'Dangling tokens starting with ' + token
            raise ParseException(message, self.expression, token, start, end)

    def begin(self):
        return self.add_or_sub()

    def add_or_sub(self):
        first_tree = self.mul_or_div()
        ops = []
        trees = []
        while True:
            if self.tokenizer.has_next():
                self.token, self.start, self.end = self.tokenizer.peek()
                if self.token in ('+', '-'):
                    next(self.tokenizer)
                    ops.append(self.token)
                    trees.append(self.mul_or_div())
                else:
                    break
            else:
                break
        if trees:
            result_tree = first_tree
            for op, tree in zip(ops, trees):
                result_tree = BinaryOperation(op, result_tree, tree)
            return result_tree
        else:
            return first_tree

    def mul_or_div(self):
        first_tree = self.negative()
        ops = []
        trees = []
        while True:
            if self.tokenizer.has_next():
                self.token, self.start, self.end = self.tokenizer.peek()
                if self.token in ('*', '/'):
                    next(self.tokenizer)
                    ops.append(self.token)
                    trees.append(self.negative())
                else:
                    break
            else:
                break
        if trees:
            result_tree = first_tree
            for op, tree in zip(ops, trees):
                result_tree = BinaryOperation(op, result_tree, tree)
            return result_tree
        else:
            return first_tree

    def negative(self):
        if self.tokenizer.has_next():
            self.token, self.start, self.end = self.tokenizer.peek()
            if self.token == '-':
                next(self.tokenizer)
                tree = self.negative()
                return UnaryFunction('-', tree)
            else:
                return self.exponent()
            pass
        else:
            message = 'Expected token after ' + self.token
            expression = self.expression
            token = self.token
            start = self.start
            end = self.end
            raise ParseException(message, expression, token, start, end)

    def exponent(self):
        left_tree = self.factorial()
        if self.tokenizer.has_next():
            self.token, self.start, self.end = self.tokenizer.peek()
            if self.token == '^':
                next(self.tokenizer)
                right_tree = self.negative()
                return BinaryOperation('^', left_tree, right_tree)
        return left_tree

    def factorial(self):
        first_tree = self.atom()
        num_factorial = 0
        while True:
            if self.tokenizer.has_next():
                self.token, self.start, self.end = self.tokenizer.peek()
                if self.token == '!':
                    next(self.tokenizer)
                    num_factorial += 1
                else:
                    break
            else:
                break
        if num_factorial:
            result_tree = first_tree
            for _ in range(num_factorial):
                result_tree = UnaryFunction('!', result_tree)
            return result_tree
        else:
            return first_tree

    def atom(self):
        if self.tokenizer.has_next():
            self.token, self.start, self.end = self.tokenizer.peek()
            if is_function(self.token):
                return self.function()
            elif is_variable(self.token):
                return self.variable()
            elif is_int(self.token):
                return self.int_number()
            elif is_float(self.token):
                return self.float_number()
            else:
                return self.enclosure()
        else:
            message = 'Expected token after ' + self.token
            line = self.expression
            token = self.token
            start = self.start
            end = self.end
            raise ParseException(message, line, token, start, end)

    def enclosure(self):
        self.token, self.start, self.end = self.tokenizer.peek()
        if self.token == '(':
            next(self.tokenizer)
            return self.parentheses()
        elif self.token == '|':
            next(self.tokenizer)
            return self.absolute_value()
        else:
            message = 'Expected token after ' + self.token
            expression = self.expression
            token = self.token
            start = self.start
            end = self.end
            raise ParseException(message, expression, token, start, end)

    def parentheses(self):
        tree = self.begin()
        if self.tokenizer.has_next():
            token, start, end = self.tokenizer.peek()
            if token == ')':
                next(self.tokenizer)
                return tree
            else:
                error = 'Expected closing parenthesis, but found ' + token
                raise ParseException(error, self.expression, token, start, end)
        else:
            message = 'Expected closing parenthesis after ' + self.token
            expression = self.expression
            token = self.token
            start = self.start
            end = self.end
            raise ParseException(message, expression, token, start, end)

    def absolute_value(self):
        tree = self.begin()
        if self.tokenizer.has_next():
            token, start, end = self.tokenizer.peek()
            if token == '|':
                next(self.tokenizer)
                return UnaryFunction('abs', tree)
            else:
                error = 'Expected closing absolute value delimiter, '\
                    'but found ' + token
                raise ParseException(error, self.expression, token, start, end)
        else:
            message = 'Expected closing absolute value delimiter '\
                'after ' + self.token
            expression = self.expression
            token = self.token
            start = self.start
            end = self.end
            raise ParseException(message, expression, token, start, end)

    def function(self):
        token, _, _ = next(self.tokenizer)
        tree = self.enclosure()
        return UnaryFunction(token, tree)

    def variable(self):
        token, start, end = next(self.tokenizer)
        if token in self.illegal_vars:
            message = 'Illegal variable name: ' + token
            raise ParseException(message, self.expression, token, start, end)
        return Variable(token)

    def int_number(self):
        token, _, _ = next(self.tokenizer)
        return Value(int(token))

    def float_number(self):
        token, _, _ = next(self.tokenizer)
        return Value(float(token))