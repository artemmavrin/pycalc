from src.test import ConsoleTest
from src.tokenizer import Tokenizer, underline_token

@ConsoleTest
def test_tokenizer(line):
    tokenizer = Tokenizer(line)
    for _, start, end in tokenizer:
        underline_token(line, start, end)

if __name__ == '__main__':
    test_tokenizer()