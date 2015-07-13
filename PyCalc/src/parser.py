from src.tokenizer import Tokenizer

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

class Parser(object):
    def parse(self, line):
        self.tokens = Tokenizer(line)
        self.tree = self.start()
    
    def start(self):
        pass
    
    def add_or_sub(self):
        pass
    
    def mul_or_div(self):
        pass
    
    def negative(self):
        pass
    
    def exponent(self):
        pass
    
    def atom(self):
        pass
    
    def enclosure(self):
        pass
    
    def parentheses(self):
        pass
    
    def absolute_value(self):
        pass
    
    def function(self):
        pass
    
    def variable(self):
        pass
    
    def int_number(self):
        pass
    
    def float_number(self):
        pass
