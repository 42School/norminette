import unittest
import sys
from lexer.lexer import Lexer


def eat_tokens(line):
    lex = Lexer(line)
    line = ""
    while lex.get_next_token():
        line += lex.peek_token().test()
        if lex.peek_token().type in ["EOF", "ERROR"]:
            break
    return line


class IdentifiersTokensTest(unittest.TestCase):

    def test_simple_identifier(self):
        self.assertEqual(eat_tokens("foo"), "<IDENTIFIER=foo>")

    def test_underscore_identifier(self):
        self.assertEqual(eat_tokens("_foo"), "<IDENTIFIER=_foo>")

    def test_underscore_with_number_identifier(self):
        self.assertEqual(eat_tokens("_foo42"), "<IDENTIFIER=_foo42>")

    def test_double_underscore_with_number_identifier(self):
        self.assertEqual(eat_tokens("_foo__42"), "<IDENTIFIER=_foo__42>")

    def test_underscore_and_uppercase_identifier(self):
        self.assertEqual(eat_tokens("_FOO"), "<IDENTIFIER=_FOO>")

    def test_underscore_at_the_end_and_uppercase_identifier(self):
        self.assertEqual(eat_tokens("FOO_"), "<IDENTIFIER=FOO_>")

    def test_identifier_can_not_start_with_a_number(self):
        self.assertNotEqual(eat_tokens("5_FOO_"), "<IDENTIFIER=5_FOO_>")

    def test_identifier_can_not_have_a_space(self):
        self.assertNotEqual(eat_tokens("foo 1"), "<IDENTIFIER=foo 1")

    def test_31_characters(self):
        self.assertEqual(
                eat_tokens("this_is_a_very_long_identifier_"),
                "<IDENTIFIER=this_is_a_very_long_identifier_>")
