'''
The grammar for the PyCalc language is as follows:

start ::= add_or_sub

add_or_sub ::= mul_or_div (('+'|'-') mul_or_div)*

mul_or_div ::= negative (('*'|'/') negative)*

negative ::= exponent | '-' negative

exponent ::= atom | atom '^' negative

atom ::= function | variable | int_number | float_number | enclosure

enclosure ::= parentheses | absolute_value

parentheses ::= '(' start ')'

absolute_value ::= '|' start '|'

function ::= <valid function name> enclosure

variable ::= <valid variable name>

int_number ::= <int>

float_number ::= <float>
'''
from src.lang import is_float, is_function, is_int, is_variable
from src.tokenizer import Tokenizer
from src.tree import BinaryOperation, UnaryFunction, Value, Variable


class ParseException(Exception):
    def __init__(self, message, line, token, start, end):
        super().__init__(message)
        super.line = line
        super.token = token
        super.start = start
        super.end = end

class Parser(object):
    def parse(self, line):
        self.tokens = Tokenizer(line)
        self.tree = self.start()
    
    def start(self):
        return self.add_or_sub()
    
    def add_or_sub(self):
        first_tree = self.mul_or_div()
        ops = []
        trees = []
        while True:
            if self.tokens.has_next():
                op, _, _ = self.tokens.peek()
                if op in ('+', '-'):
                    next(self.tokens)
                    ops.append(op)
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
            if self.tokens.has_next():
                op, _, _ = self.tokens.peek()
                if op in ('*', '/'):
                    next(self.tokens)
                    ops.append(op)
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
        if self.tokens.has_next():
            token, _, _ = self.tokens.peek()
            if token == '-':
                next(self.tokens)
                tree = self.negative()
                return UnaryFunction(token, tree)
            else:
                return self.exponent()
            pass
        else:
            raise Exception #TODO: handle exception
    
    def exponent(self):
        left_tree = self.atom()
        if self.tokens.has_next():
            token, _, _ = self.tokens.peek()
            if token == '^':
                next(self.tokens)
                right_tree = self.negative()
                return BinaryOperation(token, left_tree, right_tree)
        return left_tree
    
    def atom(self):
        token, _, _ = self.tokens.peek()
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
        token, _, _ = self.tokens.peek()
        if token == '(':
            next(self.tokens)
            return self.parentheses()
        elif token == '|':
            next(self.tokens)
            return self.absolute_value()
        else:
            raise Exception #TODO: Handle exception
    
    def parentheses(self):
        tree = self.start()
        if self.tokens.has_next():
            token, _, _ = self.tokens.peek()
            if token == ')':
                next(self.tokens)
                return tree
            else:
                raise Exception #TODO: Handle exception
        else:
            raise Exception #TODO: Handle exception
    
    def absolute_value(self):
        tree = self.start()
        if self.tokens.has_next():
            token, _, _ = self.tokens.peek()
            if token == '|':
                next(self.tokens)
                return UnaryFunction('abs', tree)
            else:
                raise Exception #TODO: Handle exception
        else:
            raise Exception #TODO: Handle exception
    
    def function(self):
        token, _, _ = next(self.tokens)
        tree = self.enclosure()
        return UnaryFunction(token, tree)
    
    def variable(self):
        token, _, _ = next(self.tokens)
        return Variable(token)
    
    def int_number(self):
        token, _, _ = next(self.tokens)
        return Value(int(token))
    
    def float_number(self):
        token, _, _ = next(self.tokens)
        return Value(float(token))
