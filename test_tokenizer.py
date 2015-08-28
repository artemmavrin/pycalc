from tokenizer import generate_tokens
from misc import underline_substring
from test import ConsoleTest


@ConsoleTest
def test_tokenizer(line):
    for token, _, _ in generate_tokens(line):
        print(token)

if __name__ == '__main__':
    test_tokenizer()
