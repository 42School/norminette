import unittest
import sys
from lexer.lexer import Lexer, TokenError


class CharConstTokenTest(unittest.TestCase):
    def assertRaises(self, test):
        try:
            test()
            return False
        except TokenError:
            return True

    def test_basic_char(self):
        self.assertEqual(
            Lexer("'*'").get_next_token().test(),
            "<CHAR_CONST='*'>")

    def test_escaped_newline(self):
        self.assertEqual(
            Lexer("'\\n'").get_next_token().test(),
            "<CHAR_CONST='\\n'>")

    def test_octal_char(self):
        self.assertEqual(
            Lexer("'\\042'").get_next_token().test(),
            "<CHAR_CONST='\\042'>")

    def test_hex_char(self):
        self.assertEqual(
            Lexer("'0x042'").get_next_token().test(),
            "<CHAR_CONST='0x042'>")

    def test_hex_char(self):
        self.assertEqual(
            Lexer("'0x042'").get_next_token().test(),
            "<CHAR_CONST='0x042'>")

    def test_error_newline_in_const(self):
        self.assertRaises(Lexer("'\n1'").get_next_token)

    def test_error_escaped_newline_followed_by_newline(self):
        self.assertRaises(Lexer("'\\n\n'").get_next_token)

    def test_error_unclosed_quote(self):
        self.assertRaises(Lexer("'A").get_next_token)


if __name__ == '__main__':
    unittest.main()
