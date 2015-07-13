from collections import Hashable
from itertools import chain
from functools import reduce
from operator import mul

class Peeker(object):
    def __init__(self, iterable):
        self.iterable = iter(iterable)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        return next(self.iterable)
    
    def peek(self):
        peek_value = next(self)
        self.iterable = chain([peek_value], self.iterable)
        return peek_value
    
    def has_next(self):
        try:
            self.peek()
            return True
        except StopIteration:
            return False


class Memoize(object):
    def __init__(self, f):
        self.f = f
        self.cache = {}
    
    def __call__(self, *args):
        if not isinstance(args, Hashable):
            return self.f(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.f(*args)
            self.cache[args] = value
            return value


@Memoize
def factorial(n):
    if n == 0:
        return 1
    else:
        try:
            # Could cause a runtime exception if the recursion is too deep
            return n * factorial(n-1)
        except RuntimeError:
            return reduce(mul, range(1,n+1))
