def print_table(table, sep=' '):
    '''Print a table (a list of lists) with proper column spacing.'''
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


def print_iterable(iterable, max_length=80, sep=' ', end='\n'):
    '''Pretty-print an iterable object to the console.

    Args:
        iterable : iterable
            The iterable object to be printed
        max_length : int (optional)
            The width of the console.
        sep : str (optional)
            The separator to be printed in between elements of the iterator.
        end : str (optional)
            The string to print at the end.
    '''
    spaces_used = 0
    xs = iter(iterable)
    try:
        x = next(xs)
    except StopIteration:
        pass
    else:
        while True:
            try:
                y = next(xs)
                current = str(x) + sep
                if spaces_used + len(current) > max_length:
                    print()
                    spaces_used = 0
                print(current, end='')
                spaces_used += len(current)
                x = y
            except StopIteration:
                current = str(x) + end
                if spaces_used + len(current) > max_length:
                    print()
                    spaces_used = 0
                print(current, end='')
                spaces_used += len(current)
                break


def underline_substring(string, start, end, underline_char='^'):
    '''Print a string to the console and highlight a segment of it on the next
    line.'''
    print(string)
    print(start * ' ' + (end - start) * underline_char)
