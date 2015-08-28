from parser import Parser, ParseException
from misc import underline_substring
from test import ConsoleTest


@ConsoleTest
def test_parser(line):
    parser = Parser()
    try:
        parser.parse(line)
    except ParseException as ex:
        print('Error:', str(ex))
        underline_substring(line, ex.start, ex.end)
    else:
        tree = parser.tree
        print(tree)

if __name__ == '__main__':
    test_parser()
