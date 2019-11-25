import unittest
import sys
from lexer import Lexer

sys.path.append('../..')


class CharConstTokenTest(unittest.TestCase):

    def test_basic_char(self):
        self.assertEqual(
            Lexer("'*'").getNextToken().test(),
            "<CHAR_CONST='*'>")

    def test_escaped_newline(self):
        self.assertEqual(
            Lexer("'\\n'").getNextToken().test(),
            "<CHAR_CONST='\\n'>")

    def test_octal_char(self):
        self.assertEqual(
            Lexer("'\\042'").getNextToken().test(),
            "<CHAR_CONST='\\042'>")

    def test_hex_char(self):
        self.assertEqual(
            Lexer("'0x042'").getNextToken().test(),
            "<CHAR_CONST='0x042'>")


if __name__ == '__main__':
    unittest.main()
