from pycalc.lang import reserved_chars
from pycalc.misc import Peeker


def generate_tokens(line, start=0):
    if start < len(line):
        token = line[start]
        if token == ' ':
            yield from generate_tokens(line, start + 1)
        elif token in reserved_chars:
            yield token, start, start + 1
            yield from generate_tokens(line, start + 1)
        else:
            end = start + 1
            while end < len(line):
                if line[end] in reserved_chars or line[end] == ' ':
                    break
                end += 1
            yield line[start:end], start, end
            yield from generate_tokens(line, end)


def underline_token(line, start, end):
    print(line)
    print(start * ' ' + (end - start) * '^')


class Tokenizer(Peeker):
    def __init__(self, line):
        super().__init__(generate_tokens(line))
