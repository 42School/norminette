import unittest
import sys
from lexer.lexer import Lexer


class BracketsTokensTest(unittest.TestCase):

    def test_opening_bracket(self):
        self.assertEqual(
                        Lexer("{").getNextToken().type,
                        "LBRACE")

    def test_closing_bracket(self):
        self.assertEqual(Lexer("}").getNextToken().type, "RBRACE")

    def test_opening_parenthesis(self):
        self.assertEqual(Lexer("(").getNextToken().type, "LPARENTHESIS")

    def test_closing_parenthesis(self):
        self.assertEqual(Lexer(")").getNextToken().type, "RPARENTHESIS")

    def test_opening_square_bracket(self):
        self.assertEqual(
                        Lexer("[").getNextToken().type,
                        "LBRACKET")

    def test_closing_square_bracket(self):
        self.assertEqual(
                        Lexer("]").getNextToken().type,
                        "RBRACKET")


if __name__ == '__main__':
    unittest.main()
