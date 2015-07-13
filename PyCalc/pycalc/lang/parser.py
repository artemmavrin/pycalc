'''
The grammar for the PyCalc language is as follows:

begin ::= add_or_sub

add_or_sub ::= mul_or_div (('+'|'-') mul_or_div)*

mul_or_div ::= negative (('*'|'/') negative)*

negative ::= exponent | '-' negative

exponent ::= factorial | factorial '^' negative

factorial ::= atom

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
from pycalc.lang.tokenizer import Tokenizer
from pycalc.lang.tree import BinaryOperation, UnaryFunction, Value, Variable


class ParseException(Exception):
    def __init__(self, message, line, token, start, end):
        super().__init__(message)
        super.line = line
        super.token = token
        super.start = start
        super.end = end


class Parser(object):
    def parse(self, line):
        self.tokenizer = Tokenizer(line)
        self.tree = self.begin()
    
    def begin(self):
        return self.add_or_sub()
    
    def add_or_sub(self):
        first_tree = self.mul_or_div()
        ops = []
        trees = []
        while True:
            if self.tokenizer.has_next():
                token, _, _ = self.tokenizer.peek()
                if token in ('+', '-'):
                    next(self.tokenizer)
                    ops.append(token)
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
                token, _, _ = self.tokenizer.peek()
                if token in ('*', '/'):
                    next(self.tokenizer)
                    ops.append(token)
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
            token, _, _ = self.tokenizer.peek()
            if token == '-':
                next(self.tokenizer)
                tree = self.negative()
                return UnaryFunction(token, tree)
            else:
                return self.exponent()
            pass
        else:
            raise Exception #TODO: handle exception
    
    def exponent(self):
        left_tree = self.factorial()
        if self.tokenizer.has_next():
            token, _, _ = self.tokenizer.peek()
            if token == '^':
                next(self.tokenizer)
                right_tree = self.negative()
                return BinaryOperation(token, left_tree, right_tree)
        return left_tree
    
    def factorial(self):
        #TODO: Implement grammar rule
        return self.atom()
    
    def atom(self):
        token, _, _ = self.tokenizer.peek()
        if is_function(token):
            return self.function()
        elif is_variable(token):
            return self.variable()
        elif is_int(token):
            return self.int_number()
        elif is_float(token):
            return self.float_number()
        else:
            return self.enclosure()
    
    def enclosure(self):
        token, _, _ = self.tokenizer.peek()
        if token == '(':
            next(self.tokenizer)
            return self.parentheses()
        elif token == '|':
            next(self.tokenizer)
            return self.absolute_value()
        else:
            raise Exception #TODO: Handle exception
    
    def parentheses(self):
        tree = self.begin()
        if self.tokenizer.has_next():
            token, _, _ = self.tokenizer.peek()
            if token == ')':
                next(self.tokenizer)
                return tree
            else:
                raise Exception #TODO: Handle exception
        else:
            raise Exception #TODO: Handle exception
    
    def absolute_value(self):
        tree = self.begin()
        if self.tokenizer.has_next():
            token, _, _ = self.tokenizer.peek()
            if token == '|':
                next(self.tokenizer)
                return UnaryFunction('abs', tree)
            else:
                raise Exception #TODO: Handle exception
        else:
            raise Exception #TODO: Handle exception
    
    def function(self):
        token, _, _ = next(self.tokenizer)
        tree = self.enclosure()
        return UnaryFunction(token, tree)
    
    def variable(self):
        token, _, _ = next(self.tokenizer)
        return Variable(token)
    
    def int_number(self):
        token, _, _ = next(self.tokenizer)
        return Value(int(token))
    
    def float_number(self):
        token, _, _ = next(self.tokenizer)
        return Value(float(token))
