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