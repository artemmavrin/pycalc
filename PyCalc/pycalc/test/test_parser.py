from pycalc.lang.parser import Parser, ParseException
from pycalc.test import ConsoleTest
from pycalc.lang.tokenizer import underline_token


@ConsoleTest
def test_parser(line):
    parser = Parser()
    try:
        parser.parse(line)
    except ParseException as ex:
        print('Error:', str(ex))
        underline_token(line, ex.start, ex.end)
    else:
        tree = parser.tree
        print(tree)
        variables = {}
        if tree.set_variables(variables):
            print(tree.evaluate())

if __name__ == '__main__':
    test_parser()
