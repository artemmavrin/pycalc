from abc import ABCMeta, abstractmethod

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


class Branch(AST):
    def __init__(self, f, identifier, *args):
        self.f = f
        self.identifier = identifier
        self.args = args
    
    def evaluate(self):
        return self.f(*(arg.evaluate() for arg in self.args))
    
    def postfix(self):
        arguments = ' '.join(arg.postfix() for arg in self.args)
        return '(' + arguments + ') ' + self.identifier