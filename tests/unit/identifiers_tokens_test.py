import unittest
import sys
from lexer import Lexer

sys.path.append('../..')


class IdentifiersTokensTest(unittest.TestCase):

    def test_simple_identifier(self):
        self.assertEqual(Lexer("foo").getNextToken().type, "IDENTIFIER")

    def test_underscore_identifier(self):
        self.assertEqual(Lexer("_foo").getNextToken().type, "IDENTIFIER")

    def test_underscore_with_number_identifier(self):
        self.assertEqual(Lexer("_foo42").getNextToken().type, "IDENTIFIER")

    def test_double_underscore_with_number_identifier(self):
        self.assertEqual(Lexer("_foo__42").getNextToken().type, "IDENTIFIER")

    def test_underscore_and_uppercase_identifier(self):
        self.assertEqual(Lexer("_FOO").getNextToken().type, "IDENTIFIER")

    def test_underscore_at_the_end_and_uppercase_identifier(self):
        self.assertEqual(Lexer("FOO_").getNextToken().type, "IDENTIFIER")

    def test_identifier_can_not_start_with_a_number(self):
        self.assertNotEqual(Lexer("5_FOO_").getNextToken().type, "IDENTIFIER")

    def test_31_characters(self):
        self.assertEqual(
                Lexer("this_is_a_very_long_identifier_").getNextToken().type,
                "IDENTIFIER")

    def test_only_31_characters_are_significant(self):
        self.assertNotEqual(
                Lexer("this_is_a_very_long_identifier_this_should_not_count")
                .getNextToken().type,
                "IDENTIFIER")
