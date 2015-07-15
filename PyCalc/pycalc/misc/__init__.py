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


def print_table(table, sep=' '):
    table = list(table)
    if table:
        # check if each row in the table has the same number of items
        if min(len(row) for row in table) != max(len(row) for row in table):
            raise Exception('Each row in the table must have the same length')
        max_len = list(0 for _ in table[0])
        for row in table:
            row_len = list(len(str(item)) for item in row)
            max_len = list(max(a, b) for a, b in zip(max_len, row_len))

        format_string = sep.join('{:<' + str(l) + '}' for l in max_len)
        for row in table:
            print(format_string.format(*row))


def print_iterable(iterable, max_length=80, sep=' '):
    spaces_used = 0
    for x in iter(iterable):
        current_string = str(x) + sep
        if spaces_used + len(current_string) > max_length:
            print()
            spaces_used = 0
        print(current_string, end="")
        spaces_used += len(current_string)
