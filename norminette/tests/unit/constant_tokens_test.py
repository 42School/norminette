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
        self.assertEqual(Lexer("42").checkTokens(), "<CONSTANT=42>\n")

    def test_plus_sign_constant(self):
        self.assertEqual(
                        Lexer("+42").checkTokens(),
                        "<OP_PLUS><CONSTANT=42>\n")

    def test_minus_sign_constant(self):
        self.assertEqual(
                        Lexer("-42").checkTokens(),
                        "<OP_MINUS><CONSTANT=42>\n")

    def test_many_signs_constant(self):
        self.assertEqual(
                        Lexer("+-42").checkTokens(),
                        "<OP_PLUS><OP_MINUS><CONSTANT=42>\n")

    def test_decimal_constant(self):
        self.assertEqual(
                        Lexer("4.2").checkTokens(),
                        "<CONSTANT=4.2>\n")

    def test_decimal_constant_starting_with_dot(self):
        self.assertEqual(
                        Lexer(".42").checkTokens(),
                        "<CONSTANT=.42>\n")

    def test_exponential_constant(self):
        self.assertEqual(
                        Lexer("4e2").checkTokens(),
                        "<CONSTANT=4e2>\n")

    def test_exponential_constant_starting_with_dot(self):
        self.assertEqual(
                        Lexer(".4e2").checkTokens(),
                        "<CONSTANT=.4e2>\n")

    def test_octal_constant(self):
        self.assertEqual(
                        Lexer("042").checkTokens(),
                        "<CONSTANT=042>\n")

    def test_hex_constant(self):
        self.assertEqual(
                        Lexer("0x42").checkTokens(),
                        "<CONSTANT=0x42>\n")

    def test_hex_with_sign_constant(self):
        self.assertEqual(
                        Lexer("-0x4e2").checkTokens(),
                        "<OP_MINUS><CONSTANT=0x4e2>\n")

    def test_hex_with_many_signs_constant(self):
        self.assertEqual(
                        Lexer("-+-+-+-+-+-+-+-0Xe4Ae2").checkTokens(),
                        "<OP_MINUS><OP_PLUS><OP_MINUS><OP_PLUS><OP_MINUS>"
                        + "<OP_PLUS><OP_MINUS><OP_PLUS><OP_MINUS><OP_PLUS>"
                        + "<OP_MINUS><OP_PLUS><OP_MINUS><OP_PLUS><OP_MINUS>"
                        + "<CONSTANT=0Xe4Ae2>\n")

    def test_long_constant(self):
        self.assertEqual(
                        Lexer("42l").checkTokens(),
                        "<CONSTANT=42l>\n")

    def test_unsigned_long_constant(self):
        self.assertEqual(
                        Lexer("42ul").checkTokens(),
                        "<CONSTANT=42ul>\n")

    def test_long_long_constant(self):
        self.assertEqual(
                        Lexer("42ll").checkTokens(),
                        "<CONSTANT=42ll>\n")

    def test_unsigned_long_long_constant(self):
        self.assertEqual(
                        Lexer("42ull").checkTokens(),
                        "<CONSTANT=42ull>\n")

    def test_unsigned_constant(self):
        self.assertEqual(
                        Lexer("42u").checkTokens(),
                        "<CONSTANT=42u>\n")

    def test_unsigned_mixed_caps_constant(self):
        self.assertEqual(
                        Lexer("42uLl").checkTokens(),
                        "<CONSTANT=42uLl>\n")

    def test_unsigned_mixed_caps_constant_2(self):
        self.assertEqual(
                        Lexer("42ULl").checkTokens(),
                        "<CONSTANT=42ULl>\n")

    def test_unsigned_mixed_caps_and_hex_constant(self):
        self.assertEqual(
                        Lexer("0x42UlL").checkTokens(),
                        "<CONSTANT=0x42UlL>\n")

    def test_error_too_many_dots(self):
        self.assertRaises(Lexer("4.4.4").checkTokens)

    def test_error_too_many_e(self):
        self.assertRaises(Lexer("4e4e4").checkTokens)

    def test_error_too_many_x(self):
        self.assertRaises(Lexer("4x4x4").checkTokens)

    def test_error_too_many_u(self):
        self.assertRaises(Lexer("42uul").checkTokens)

    def test_error_too_many_l(self):
        self.assertRaises(Lexer("42Lllu").checkTokens)

    def test_error_misplaced_l(self):
        self.assertRaises(Lexer("42lul").checkTokens)

    def test_misplaced_e(self):
        self.assertEqual(
                        Lexer(".e42").checkTokens(),
                        "<OP_DOT><IDENTIFIER=e42>\n")

    def test_another_misplaced_e(self):
        self.assertRaises(Lexer(".42e").checkTokens)


if __name__ == '__main__':
    unittest.main()
