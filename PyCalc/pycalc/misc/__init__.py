from itertools import chain


class Peeker(object):
    '''Class for peeking at the next element of an iterator.

    Example:
    >>> peeker = Peeker(range(2))
    >>> peeker.has_next()
    True
    >>> peeker.peek()
    0
    >>> next(peeker)
    0
    >>> peeker.has_next()
    True
    >>> peeker.peek()
    1
    >>> next(peeker)
    1
    >>> peeker.has_next()
    False
    >>> peeker.peek()
    Traceback (most recent call last):
    ...
    StopIteration

    '''

    def __init__(self, iterable):
        self.iterator = iter(iterable)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.iterator)

    def peek(self):
        peek_value = next(self)
        self.iterator = chain([peek_value], self.iterator)
        return peek_value

    def has_next(self):
        try:
            self.peek()
            return True
        except StopIteration:
            return False
