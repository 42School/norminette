import unittest
import sys
from lexer import Lexer


sys.path.append('../..')


def eat_token_line(line):
    lex = Lexer(line)
    line = ""
    while lex.getNextToken():
        line += lex.peekToken().test()
        if lex.peekToken().type is "EOF":
            break
    return line


class TokensLinesTest(unittest.TestCase):
    def test_basic_line(self):
        self.maxDiff = None
        inpt = "int a = 42;\n"
        output = "<INT><SPACE><IDENTIFIER=a><SPACE><OP_ASSIGN>" \
            + "<SPACE><CONSTANT=42><OP_SEMI_COLON><NEWLINE><EOF>"
        self.assertEqual(eat_token_line(inpt), output)

    def test_tricky_operators_on_line(self):
        self.maxDiff = None
        inpt = "int a = +-+-42 * (-42+ -+-+42);\n"
        output = "<INT><SPACE><IDENTIFIER=a><SPACE><OP_ASSIGN><SPACE>" \
            + "<CONSTANT=+-+-42><SPACE><OP_MULT><SPACE>" \
            + "<OPENING_PARENTHESIS><CONSTANT=-42><OP_PLUS>" \
            + "<SPACE><CONSTANT=-+-+42><CLOSING_PARENTHESIS>" \
            + "<OP_SEMI_COLON><NEWLINE><EOF>"
        self.assertEqual(eat_token_line(inpt), output)

    def test_function_prototype_without_newline(self):
        self.maxDiff = None
        inpt = "void\tfoo(int a, char *b, ...);"
        output = "<VOID><TAB><IDENTIFIER=foo><OPENING_PARENTHESIS><INT>" \
            + "<SPACE><IDENTIFIER=a><OP_COMMA><SPACE><CHAR><SPACE>" \
            + "<OP_MULT><IDENTIFIER=b><OP_COMMA><SPACE><OP_ELLIPSIS>" \
            + "<CLOSING_PARENTHESIS><OP_SEMI_COLON><EOF>"
        self.assertEqual(eat_token_line(inpt), output)


if __name__ == '__main__':
    unittest.main()
