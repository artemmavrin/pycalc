from itertools import chain


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
