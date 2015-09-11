'''Module containg Abstract Syntax Tree (AST) constructors.'''
from abc import ABCMeta, abstractmethod
from math import exp, log, cos, sin, tan, factorial
from operator import add, sub, mul, truediv, pow, neg


# Binary operation lookup table (prevents looking at cases later).
bin_ops = {
           '+': add,
           '-': sub,
           '*': mul,
           '/': truediv,
           '^': pow
           }

# Function lookup table (also prevents looking at cases later).
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
    '''Abstract AST class.'''
    @abstractmethod
    def evaluate(self):
        '''Traverse the tree and return the value that the tree represents.'''
        # Implemented in subclass.
        pass

    @abstractmethod
    def set_variables(self, variables):
        '''Assign values to variables in the leaf nodes.'''
        # Implemented in subclass.
        pass

    @abstractmethod
    def postfix(self):
        '''Return a postfix (postorder) representation of the tree.'''
        # Implemented in subclass.
        pass

    def __repr__(self):
        '''Convert the tree to a string.'''
        return self.postfix()


class Branch(AST, metaclass=ABCMeta):
    '''A branch of the AST. The value of a branch is a function. Children of the
    branch are ASTs which represent arguments to the function.'''
    def __init__(self, f, identifier, *args):
        self.f = f
        self.identifier = identifier
        self.args = args

    def evaluate(self):
        '''Evaluate the children, then apply the function to the results.'''
        return self.f(*(arg.evaluate() for arg in self.args))

    def set_variables(self, variables):
        return all(arg.set_variables(variables) for arg in self.args)

    def postfix(self):
        arguments = ' '.join(arg.postfix() for arg in self.args)
        return '(' + arguments + ') ' + self.identifier


class BinaryOperation(Branch):
    '''A type of AST Branch where the node is a binary operation and there are
    two children.'''
    def __init__(self, op_symbol, left, right):
        # Check if bin_op is one of the available binary operations.
        if op_symbol in bin_ops:
            bin_op = bin_ops[op_symbol]
            super().__init__(bin_op, op_symbol, left, right)
        else:
            raise ValueError('Illegal binary operation: ' + op_symbol)


class UnaryFunction(Branch):
    '''A type of AST Branch where the node is a unary function and there is only
    one child AST.'''
    def __init__(self, function_name, argument):
        # Check if function_name is one of the available functions.
        if function_name in functions:
            function = functions[function_name]
            super().__init__(function, function_name, argument)
        else:
            raise ValueError('Illegal function: ' + function_name)


class Leaf(AST, metaclass=ABCMeta):
    '''A node on an AST with no children.'''
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
    '''A leaf with a constant numeric value.'''
    def __init__(self, value):
        super().__init__(str(value), value)


class Variable(Leaf):
    '''A leaf with a variable value.'''
    def __init__(self, name):
        super().__init__(name, None)

    def evaluate(self):
        # Check if the variable name is assigned to a value.
        if self.value is not None:
            return self.value
        else:
            message = 'The variable ' + self.name + ' has no value.'
            raise UnboundLocalError(message)

    def set_variables(self, variables):
        # Try to assign a value to the variable name.
        if self.name in variables:
            self.value = variables[self.name]
            return True
        else:
            return False
