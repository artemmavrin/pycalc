from src.test import ConsoleTest
from src.parser import Parser

@ConsoleTest
def test_parser(line):
    parser = Parser()
    parser.parse(line)
    tree = parser.tree
    print(tree)

if __name__ == '__main__':
    test_parser()