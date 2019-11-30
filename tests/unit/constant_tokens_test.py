import unittest
import sys
from lexer import Lexer


def eat_tokens(line):
    lex = Lexer(line)
    line = ""
    while lex.getNextToken():
        line += lex.peekToken().test()
        if lex.peekToken().type in ["EOF", "TKN_ERROR"]:
            break
    return line


class ConstantTokensTest(unittest.TestCase):

    def test_basic_constant(self):
        self.assertEqual(
                        eat_tokens("42"),
                        "<CONSTANT=42>")

    def test_plus_sign_constant(self):
        self.assertEqual(
                        eat_tokens("+42"),
                        "<OP_PLUS><CONSTANT=42>")

    def test_minus_sign_constant(self):
        self.assertEqual(
                        eat_tokens("-42"),
                        "<OP_MINUS><CONSTANT=42>")

    def test_many_signs_constant(self):
        self.assertEqual(
                        eat_tokens("+-42"),
                        "<OP_PLUS><OP_MINUS><CONSTANT=42>")

    def test_decimal_constant(self):
        self.assertEqual(
                        eat_tokens("4.2"),
                        "<CONSTANT=4.2>")

    def test_decimal_constant_starting_with_dot(self):
        self.assertEqual(
                        eat_tokens(".42"),
                        "<CONSTANT=.42>")

    def test_exponential_constant(self):
        self.assertEqual(
                        eat_tokens("4e2"),
                        "<CONSTANT=4e2>")

    def test_exponential_constant_starting_with_dot(self):
        self.assertEqual(
                        eat_tokens(".4e2"),
                        "<CONSTANT=.4e2>")

    def test_octal_constant(self):
        self.assertEqual(
                        eat_tokens("042"),
                        "<CONSTANT=042>")

    def test_hex_constant(self):
        self.assertEqual(
                        eat_tokens("0x42"),
                        "<CONSTANT=0x42>")

    def test_hex_with_sign_constant(self):
        self.assertEqual(
                        eat_tokens("-0x4e2"),
                        "<OP_MINUS><CONSTANT=0x4e2>")

    def test_hex_with_many_signs_constant(self):
        self.assertEqual(
                        eat_tokens("-+-+-+-+-+-+-+-0Xe4Ae2"),
                        "<OP_MINUS><OP_PLUS><OP_MINUS><OP_PLUS><OP_MINUS>"
                        + "<OP_PLUS><OP_MINUS><OP_PLUS><OP_MINUS><OP_PLUS>"
                        + "<OP_MINUS><OP_PLUS><OP_MINUS><OP_PLUS><OP_MINUS>"
                        + "<CONSTANT=0Xe4Ae2>")

    def test_long_constant(self):
        self.assertEqual(
                        eat_tokens("42l"),
                        "<CONSTANT=42l>")

    def test_unsigned_long_constant(self):
        self.assertEqual(
                        eat_tokens("42ul"),
                        "<CONSTANT=42ul>")

    def test_long_long_constant(self):
        self.assertEqual(
                        eat_tokens("42ll"),
                        "<CONSTANT=42ll>")

    def test_unsigned_long_long_constant(self):
        self.assertEqual(
                        eat_tokens("42ull"),
                        "<CONSTANT=42ull>")

    def test_unsigned_constant(self):
        self.assertEqual(
                        eat_tokens("42u"),
                        "<CONSTANT=42u>")

    def test_unsigned_mixed_caps_constant(self):
        self.assertEqual(
                        eat_tokens("42uLl"),
                        "<CONSTANT=42uLl>")

    def test_unsigned_mixed_caps_constant_2(self):
        self.assertEqual(
                        eat_tokens("42ULl"),
                        "<CONSTANT=42ULl>")

    def test_unsigned_mixed_caps_and_hex_constant(self):
        self.assertEqual(
                        eat_tokens("0x42UlL"),
                        "<CONSTANT=0x42UlL>")

    def test_error_too_many_dots(self):
        self.assertEqual(
                        eat_tokens("4.4.4"),
                        "<TKN_ERROR>")

    def test_error_too_many_e(self):
        self.assertEqual(
                        eat_tokens("4e4e4"),
                        "<TKN_ERROR>")

    def test_error_too_many_x(self):
        self.assertEqual(
                        eat_tokens("4x4x4"),
                        "<TKN_ERROR>")

    def test_error_too_many_u(self):
        self.assertEqual(
                        eat_tokens("42uul"),
                        "<TKN_ERROR>")

    def test_error_too_many_l(self):
        self.assertEqual(
                        eat_tokens("42Lllu"),
                        "<TKN_ERROR>")

    def test_error_misplaced_l(self):
        self.assertEqual(
                        eat_tokens("42lul"),
                        "<TKN_ERROR>")

    def test_misplaced_e(self):
        self.assertEqual(
                        eat_tokens(".e42"),
                        "<OP_DOT><IDENTIFIER=e42>")

    def test_another_misplaced_e(self):
        self.assertEqual(
                        eat_tokens(".42e"),
                        "<TKN_ERROR>")


if __name__ == '__main__':
    unittest.main()
