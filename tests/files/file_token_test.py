import unittest
import sys
from lexer import Lexer

sys.path.append('../..')


def eat_tokens(filename):
    with open(filename) as f:
        lex = Lexer(f.read())
        output = ""
        while lex.getNextToken().type != "EOF":
            output += lex.peekToken().test()
            if lex.peekToken().type == "NEWLINE":
                output += '\n'
            if lex.peekToken().type == "TKN_ERROR":
                break
        return output

def read_file(filename):
    with open(filename) as f:
       return f.read()

class FileTokenTest(unittest.TestCase):

    def test_basic_file(self):
        self.maxDiff = None
        self.assertEqual(
                            eat_tokens("tests/files/tokenization_test1.c"),
                            read_file("tests/files/tokenization_test1.tokens"))


if __name__ == '__main__':
    unittest.main()
