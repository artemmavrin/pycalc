'''Module containing the Parser class for parsing expressions into ASTs.

The context-free grammar for the PyCalc language is as follows:

begin ::= (variable '=')* expression
expression ::= add_or_sub
add_or_sub ::= mul_or_div (('+'|'-') mul_or_div)*
mul_or_div ::= negative (('*'|'/') negative)*
negative ::= exponent | '-' negative
exponent ::= factorial | factorial '^' negative
factorial ::= atom ('!')*
atom ::= function | variable | int_number | float_number | enclosure
enclosure ::= parentheses | absolute_value
parentheses ::= '(' expression ')'
absolute_value ::= '|' expression '|'
function ::= <valid function name> enclosure
variable ::= <valid variable name>
int_number ::= <int>
float_number ::= <float>
'''
from lang import is_float, is_function, is_int, is_variable
from tokenizer import Tokenizer
from tree import BinaryOperation, UnaryFunction, Value, Variable


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
    '''Class for parsing expressions into ASTs.'''
    def __init__(self, illegal_vars, default_variable):
        self.illegal_vars = illegal_vars
        self.default_variable = default_variable

    def parse(self, line):
        '''Begin parsing the given line.'''
        # Start at the first grammar rule:
        # begin ::= (variable '=')* expression
        # Turn the line into variable names and an arithemtic expression.
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
        self.tree = self.expression()

        # the tokenizer should be out of tokens
        if self.tokenizer.has_next():
            token, start, end = next(self.tokenizer)
            message = 'Dangling tokens starting with ' + token
            raise ParseException(message, self.expression, token, start, end)

    # Everything below corresponds to the grammar rules described at the top.

    def expression(self):
        '''Rule:
        expression ::= add_or_sub'''
        return self.add_or_sub()

    def add_or_sub(self):
        '''Rule:
        add_or_sub ::= mul_or_div (("+"|"-") mul_or_div)*'''
        first_tree = self.mul_or_div()
        # Arrays for storing successive + or - operations and the tree args.
        ops = []
        trees = []
        # Run until no more + or -'s
        while True:
            if self.tokenizer.has_next():
                self.token, self.start, self.end = self.tokenizer.peek()
                if self.token in ('+', '-'):
                    # pop the token off the stack
                    next(self.tokenizer)
                    ops.append(self.token)
                    trees.append(self.mul_or_div())
                else:
                    break
            else:
                break
        if trees:
            # Combine the trees (left-associative)
            result_tree = first_tree
            for op, tree in zip(ops, trees):
                result_tree = BinaryOperation(op, result_tree, tree)
            return result_tree
        else:
            return first_tree

    def mul_or_div(self):
        '''Rule:
        mul_or_div ::= negative (("*"|"/") negative)*'''
        first_tree = self.negative()
        # Arrays for storing successive * or / operations and the tree args.
        ops = []
        trees = []
        # Run until no more * or /'s
        while True:
            if self.tokenizer.has_next():
                self.token, self.start, self.end = self.tokenizer.peek()
                if self.token in ('*', '/'):
                    # pop the token off the stack
                    next(self.tokenizer)
                    ops.append(self.token)
                    trees.append(self.negative())
                else:
                    break
            else:
                break
        if trees:
            # Combine the trees (left-associative)
            result_tree = first_tree
            for op, tree in zip(ops, trees):
                result_tree = BinaryOperation(op, result_tree, tree)
            return result_tree
        else:
            return first_tree

    def negative(self):
        '''Rule:
        negative ::= exponent | "-" negative'''
        if self.tokenizer.has_next():
            # Check for leading minus sign
            self.token, self.start, self.end = self.tokenizer.peek()
            if self.token == '-':
                next(self.tokenizer)
                tree = self.negative()
                return UnaryFunction('-', tree)
            else:
                return self.exponent()
            pass
        else:
            # There should still be tokens on the stack at this point.
            message = 'Expected token after ' + self.token
            expression = self.expression
            token = self.token
            start = self.start
            end = self.end
            raise ParseException(message, expression, token, start, end)

    def exponent(self):
        '''Rule:
        exponent ::= factorial | factorial "^" negative'''
        left_tree = self.factorial()
        if self.tokenizer.has_next():
            self.token, self.start, self.end = self.tokenizer.peek()
            if self.token == '^':
                next(self.tokenizer)
                right_tree = self.negative()
                return BinaryOperation('^', left_tree, right_tree)
        return left_tree

    def factorial(self):
        '''Rule:
        factorial ::= atom ("!")*'''
        first_tree = self.atom()
        num_factorial = 0
        # Run until no more !'s
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
        '''Rule:
        atom ::= function | variable | int_number | float_number | enclosure'''
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
            # There should still be tokens on the stack at this point.
            message = 'Expected token after ' + self.token
            line = self.expression
            token = self.token
            start = self.start
            end = self.end
            raise ParseException(message, line, token, start, end)

    def enclosure(self):
        '''Rule:
        enclosure ::= parentheses | absolute_value'''
        self.token, self.start, self.end = self.tokenizer.peek()
        if self.token == '(':
            # Pop the token off.
            next(self.tokenizer)
            return self.parentheses()
        elif self.token == '|':
            # Pop the token off.
            next(self.tokenizer)
            return self.absolute_value()
        else:
            # There should still be tokens on the stack at this point.
            message = 'Expected token after ' + self.token
            expression = self.expression
            token = self.token
            start = self.start
            end = self.end
            raise ParseException(message, expression, token, start, end)

    def parentheses(self):
        '''Rule:
        parentheses ::= "(" expression ")"'''
        tree = self.expression()
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
        '''Rule:
        absolute_value ::= "|" expression "|"''''
        tree = self.expression()
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
        '''Rule:
        function ::= <valid function name> enclosure'''
        token, _, _ = next(self.tokenizer)
        tree = self.enclosure()
        return UnaryFunction(token, tree)

    def variable(self):
        '''Rule:
        variable ::= <valid variable name>'''
        token, start, end = next(self.tokenizer)
        if token in self.illegal_vars:
            message = 'Illegal variable name: ' + token
            raise ParseException(message, self.expression, token, start, end)
        return Variable(token)

    def int_number(self):
        '''Rule:
        int_number ::= <int>'''
        token, _, _ = next(self.tokenizer)
        return Value(int(token))

    def float_number(self):
        '''Rule:
        float_number ::= <float>'''
        token, _, _ = next(self.tokenizer)
        return Value(float(token))
