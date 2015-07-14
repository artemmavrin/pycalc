from pycalc.lang.parser import Parser
from pycalc.test import ConsoleTest


@ConsoleTest
def test_parser(line):
    parser = Parser()
    parser.parse(line)
    tree = parser.tree
    print(tree)

if __name__ == '__main__':
    test_parser()
