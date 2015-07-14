from pycalc.lang.tokenizer import generate_tokens, underline_token
from pycalc.test import ConsoleTest


@ConsoleTest
def test_tokenizer(line):
    for _, start, end in generate_tokens(line):
        underline_token(line, start, end)

if __name__ == '__main__':
    test_tokenizer()