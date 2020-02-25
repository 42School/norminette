import unittest
import sys
from lexer.lexer import Lexer, TokenError


class ConstantTokensTest(unittest.TestCase):

    def assertRaises(self, test):
        try:
            test()
            return False
        except TokenError:
            return True

    def test_basic_constant(self):
        self.assertEqual(Lexer("42").check_tokens(), "<CONSTANT=42>\n")

    def test_plus_sign_constant(self):
        self.assertEqual(
                        Lexer("+42").check_tokens(),
                        "<PLUS><CONSTANT=42>\n")

    def test_minus_sign_constant(self):
        self.assertEqual(
                        Lexer("-42").check_tokens(),
                        "<MINUS><CONSTANT=42>\n")

    def test_many_signs_constant(self):
        self.assertEqual(
                        Lexer("+-42").check_tokens(),
                        "<PLUS><MINUS><CONSTANT=42>\n")

    def test_decimal_constant(self):
        self.assertEqual(
                        Lexer("4.2").check_tokens(),
                        "<CONSTANT=4.2>\n")

    def test_decimal_constant_starting_with_dot(self):
        self.assertEqual(
                        Lexer(".42").check_tokens(),
                        "<CONSTANT=.42>\n")

    def test_exponential_constant(self):
        self.assertEqual(
                        Lexer("4e2").check_tokens(),
                        "<CONSTANT=4e2>\n")

    def test_exponential_constant_starting_with_dot(self):
        self.assertEqual(
                        Lexer(".4e2").check_tokens(),
                        "<CONSTANT=.4e2>\n")

    def test_octal_constant(self):
        self.assertEqual(
                        Lexer("042").check_tokens(),
                        "<CONSTANT=042>\n")

    def test_hex_constant(self):
        self.assertEqual(
                        Lexer("0x42").check_tokens(),
                        "<CONSTANT=0x42>\n")

    def test_hex_with_sign_constant(self):
        self.assertEqual(
                        Lexer("-0x4e2").check_tokens(),
                        "<MINUS><CONSTANT=0x4e2>\n")

    def test_hex_with_many_signs_constant(self):
        self.assertEqual(
                        Lexer("-+-+-+-+-+-+-+-0Xe4Ae2").check_tokens(),
                        "<MINUS><PLUS><MINUS><PLUS><MINUS>"
                        + "<PLUS><MINUS><PLUS><MINUS><PLUS>"
                        + "<MINUS><PLUS><MINUS><PLUS><MINUS>"
                        + "<CONSTANT=0Xe4Ae2>\n")

    def test_long_constant(self):
        self.assertEqual(
                        Lexer("42l").check_tokens(),
                        "<CONSTANT=42l>\n")

    def test_unsigned_long_constant(self):
        self.assertEqual(
                        Lexer("42ul").check_tokens(),
                        "<CONSTANT=42ul>\n")

    def test_long_long_constant(self):
        self.assertEqual(
                        Lexer("42ll").check_tokens(),
                        "<CONSTANT=42ll>\n")

    def test_unsigned_long_long_constant(self):
        self.assertEqual(
                        Lexer("42ull").check_tokens(),
                        "<CONSTANT=42ull>\n")

    def test_unsigned_constant(self):
        self.assertEqual(
                        Lexer("42u").check_tokens(),
                        "<CONSTANT=42u>\n")

    def test_error_too_many_dots(self):
        self.assertRaises(Lexer("4.4.4").check_tokens)

    def test_error_too_many_e(self):
        self.assertRaises(Lexer("4e4e4").check_tokens)

    def test_error_too_many_x(self):
        self.assertRaises(Lexer("4x4x4").check_tokens)

    def test_error_too_many_u(self):
        self.assertRaises(Lexer("42uul").check_tokens)

    def test_error_too_many_l(self):
        self.assertRaises(Lexer("42Lllu").check_tokens)

    def test_error_misplaced_l(self):
        self.assertRaises(Lexer("42lul").check_tokens)

    def test_misplaced_e(self):
        self.assertEqual(
                        Lexer(".e42").check_tokens(),
                        "<DOT><IDENTIFIER=e42>\n")

    def test_another_misplaced_e(self):
        self.assertRaises(Lexer(".42e").check_tokens)


if __name__ == '__main__':
    unittest.main()
