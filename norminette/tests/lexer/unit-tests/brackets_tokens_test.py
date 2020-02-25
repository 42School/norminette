import unittest
import sys
from lexer.lexer import Lexer


class BracketsTokensTest(unittest.TestCase):

    def test_opening_bracket(self):
        self.assertEqual(
                        Lexer("{").get_next_token().type,
                        "LBRACE")

    def test_closing_bracket(self):
        self.assertEqual(Lexer("}").get_next_token().type, "RBRACE")

    def test_opening_parenthesis(self):
        self.assertEqual(Lexer("(").get_next_token().type, "LPARENTHESIS")

    def test_closing_parenthesis(self):
        self.assertEqual(Lexer(")").get_next_token().type, "RPARENTHESIS")

    def test_opening_square_bracket(self):
        self.assertEqual(
                        Lexer("[").get_next_token().type,
                        "LBRACKET")

    def test_closing_square_bracket(self):
        self.assertEqual(
                        Lexer("]").get_next_token().type,
                        "RBRACKET")


if __name__ == '__main__':
    unittest.main()
