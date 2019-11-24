import unittest
import sys
from lexer import Lexer


sys.path.append('../..')


class ConstantTokensTest(unittest.TestCase):

    def test_basic_constant(self):
        self.assertEqual(
                        Lexer("42").getNextToken().test(),
                        "<CONSTANT=42>")

    def test_plus_sign_constant(self):
        self.assertEqual(
                        Lexer("+42").getNextToken().test(),
                        "<CONSTANT=+42>")

    def test_minus_sign_constant(self):
        self.assertEqual(
                        Lexer("-42").getNextToken().test(),
                        "<CONSTANT=-42>")

    def test_many_signs_constant(self):
        self.assertEqual(
                        Lexer("+-+-+-+-+-+-+-+-+-+-42").getNextToken().test(),
                        "<CONSTANT=+-+-+-+-+-+-+-+-+-+-42>")

    def test_decimal_constant(self):
        self.assertEqual(
                        Lexer("4.2").getNextToken().test(),
                        "<CONSTANT=4.2>")

    def test_decimal_constant_starting_with_dot(self):
        self.assertEqual(
                        Lexer(".42").getNextToken().test(),
                        "<CONSTANT=.42>")

    def test_exponential_constant(self):
        self.assertEqual(
                        Lexer("4e2").getNextToken().test(),
                        "<CONSTANT=4e2>")

    def test_exponential_constant_starting_with_dot(self):
        self.assertEqual(
                        Lexer(".4e2").getNextToken().test(),
                        "<CONSTANT=.4e2>")

    def test_octal_constant(self):
        self.assertEqual(
                        Lexer("042").getNextToken().test(),
                        "<CONSTANT=042>")

    def test_hex_constant(self):
        self.assertEqual(
                        Lexer("0x42").getNextToken().test(),
                        "<CONSTANT=0x42>")

    def test_hex_with_sign_constant(self):
        self.assertEqual(
                        Lexer("-0x4e2").getNextToken().test(),
                        "<CONSTANT=-0x4e2>")

    def test_hex_and_exponential_with_many_signs_constant(self):
        self.assertEqual(
                        Lexer("-+-+-+-+-+-+-+-0Xe4Ae2").getNextToken().test(),
                        "<CONSTANT=-+-+-+-+-+-+-+-0Xe4Ae2>")


if __name__ == '__main__':
    unittest.main()
