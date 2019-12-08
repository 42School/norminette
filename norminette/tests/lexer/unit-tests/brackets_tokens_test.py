import unittest
import sys
from lexer.lexer import Lexer


class BracketsTokensTest(unittest.TestCase):

    def test_opening_bracket(self):
        self.assertEqual(
                        Lexer("{").getNextToken().type,
                        "OPENING_BRACKET")

    def test_closing_bracket(self):
        self.assertEqual(Lexer("}").getNextToken().type, "CLOSING_BRACKET")

    def test_opening_parenthesis(self):
        self.assertEqual(Lexer("(").getNextToken().type, "OPENING_PARENTHESIS")

    def test_closing_parenthesis(self):
        self.assertEqual(Lexer(")").getNextToken().type, "CLOSING_PARENTHESIS")

    def test_opening_square_bracket(self):
        self.assertEqual(
                        Lexer("[").getNextToken().type,
                        "OPENING_SQUARE_BRACKET")

    def test_closing_square_bracket(self):
        self.assertEqual(
                        Lexer("]").getNextToken().type,
                        "CLOSING_SQUARE_BRACKET")


if __name__ == '__main__':
    unittest.main()
