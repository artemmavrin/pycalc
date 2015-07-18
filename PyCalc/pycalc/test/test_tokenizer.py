from pycalc.lang.tokenizer import generate_tokens
from pycalc.misc import underline_substring
from pycalc.test import ConsoleTest


@ConsoleTest
def test_tokenizer(line):
    for _, start, end in generate_tokens(line):
        underline_substring(line, start, end)

if __name__ == '__main__':
    test_tokenizer()
