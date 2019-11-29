import unittest
import sys
from lexer import Lexer


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

    def test_hex_char(self):
        self.assertEqual(
            Lexer("'0x042'").getNextToken().test(),
            "<CHAR_CONST='0x042'>")

    def test_error_newline_in_const(self):
        self.assertEqual(
            Lexer("'\n1'").getNextToken().test(),
            "<TKN_ERROR>")

    def test_error_escaped_newline_followed_by_newline(self):
        self.assertEqual(
            Lexer("'\\n\n'").getNextToken().test(),
            "<TKN_ERROR>")

    def test_error_unclosed_quote(self):
        self.assertEqual(
            Lexer("'A").getNextToken().test(),
            "<TKN_ERROR>")


if __name__ == '__main__':
    unittest.main()
