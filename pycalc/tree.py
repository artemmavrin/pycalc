from abc import ABCMeta, abstractmethod
from math import exp, log, cos, sin, tan, factorial
from operator import add, sub, mul, truediv, pow, neg


bin_ops = {
           '+': add,
           '-': sub,
           '*': mul,
           '/': truediv,
           '^': pow
           }

functions = {
             '-': neg,
             'abs': abs,
             'exp': exp,
             'log': log,
             'cos': cos,
             'sin': sin,
             'tan': tan,
             '!': factorial
             }


class AST(metaclass=ABCMeta):
    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def set_variables(self, variables):
        pass

    @abstractmethod
    def postfix(self):
        pass

    def __repr__(self):
        return self.postfix()


class Branch(AST, metaclass=ABCMeta):
    def __init__(self, f, identifier, *args):
        self.f = f
        self.identifier = identifier
        self.args = args

    def evaluate(self):
        return self.f(*(arg.evaluate() for arg in self.args))

    def set_variables(self, variables):
        return all(arg.set_variables(variables) for arg in self.args)

    def postfix(self):
        arguments = ' '.join(arg.postfix() for arg in self.args)
        return '(' + arguments + ') ' + self.identifier


class BinaryOperation(Branch):
    def __init__(self, op_symbol, left, right):
        if op_symbol in bin_ops:
            bin_op = bin_ops[op_symbol]
            super().__init__(bin_op, op_symbol, left, right)
        else:
            raise ValueError('Illegal binary operation: ' + op_symbol)


class UnaryFunction(Branch):
    def __init__(self, function_name, argument):
        if function_name in functions:
            function = functions[function_name]
            super().__init__(function, function_name, argument)
        else:
            raise ValueError('Illegal function: ' + function_name)


class Leaf(AST, metaclass=ABCMeta):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def evaluate(self):
        return self.value

    def set_variables(self, variables):
        return True

    def postfix(self):
        return self.name


class Value(Leaf):
    def __init__(self, value):
        super().__init__(str(value), value)


class Variable(Leaf):
    def __init__(self, name):
        super().__init__(name, None)

    def evaluate(self):
        if self.value is not None:
            return self.value
        else:
            message = 'The variable ' + self.name + ' has no value.'
            raise UnboundLocalError(message)

    def set_variables(self, variables):
        if self.name in variables:
            self.value = variables[self.name]
            return True
        else:
            return False
