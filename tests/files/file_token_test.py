import unittest
import sys
import glob
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

    def test_file_1(self):
        self.maxDiff = None
        self.assertEqual(
                            eat_tokens("tests/files/tokenization_test1.c"),
                            read_file("tests/files/tokenization_test1.tokens"))

    def test_file_2(self):
        self.maxDiff = None
        self.assertEqual(
                            eat_tokens("tests/files/tokenization_test2.c"),
                            read_file("tests/files/tokenization_test2.tokens"))

    def test_file_3(self):
        self.maxDiff = None
        self.assertEqual(
                            eat_tokens("tests/files/tokenization_test3.c"),
                            read_file("tests/files/tokenization_test3.tokens"))


    def test_file_4(self):
        self.maxDiff = None
        self.assertEqual(
                            eat_tokens("tests/files/tokenization_test4.c"),
                            read_file("tests/files/tokenization_test4.tokens"))

if __name__ == '__main__':
    unittest.main()
