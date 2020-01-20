import unittest
import sys
from lexer.lexer import Lexer


class TokensOperatorsTest(unittest.TestCase):

    def test_op_right_assign(self):
        self.assertEqual(Lexer(">>=").getNextToken().type, "RIGHT_ASSIGN")

    def test_op_left_assign(self):
        self.assertEqual(Lexer("<<=").getNextToken().type, "LEFT_ASSIGN")

    def test_op_add_assign(self):
        self.assertEqual(Lexer("+=").getNextToken().type, "ADD_ASSIGN")

    def test_op_sub_assign(self):
        self.assertEqual(Lexer("-=").getNextToken().type, "SUB_ASSIGN")

    def test_op_mul_assign(self):
        self.assertEqual(Lexer("*=").getNextToken().type, "MUL_ASSIGN")

    def test_op_div_assign(self):
        self.assertEqual(Lexer("/=").getNextToken().type, "DIV_ASSIGN")

    def test_op_mod_assign(self):
        self.assertEqual(Lexer("%=").getNextToken().type, "MOD_ASSIGN")

    def test_op_and_assign(self):
        self.assertEqual(Lexer("&=").getNextToken().type, "AND_ASSIGN")

    def test_op_xor_assign(self):
        self.assertEqual(Lexer("^=").getNextToken().type, "XOR_ASSIGN")

    def test_op_or_assign(self):
        self.assertEqual(Lexer("|=").getNextToken().type, "OR_ASSIGN")

    def test_op_le_assign(self):
        self.assertEqual(Lexer("<=").getNextToken().type, "LESS_OR_EQUAL")

    def test_op_ge_assign(self):
        self.assertEqual(Lexer(">=").getNextToken().type, "GREATER_OR_EQUAL")

    def test_op_eq_assign(self):
        self.assertEqual(Lexer("==").getNextToken().type, "EQUALS")

    def test_op_ne_assign(self):
        self.assertEqual(Lexer("!=").getNextToken().type, "NOT_EQUAL")

    def test_op_assign(self):
        self.assertEqual(Lexer("=").getNextToken().type, "ASSIGN")

    def test_op_semi_colon(self):
        self.assertEqual(Lexer(";").getNextToken().type, "SEMI_COLON")

    def test_op_colon(self):
        self.assertEqual(Lexer(":").getNextToken().type, "COLON")

    def test_op_comma(self):
        self.assertEqual(Lexer(",").getNextToken().type, "COMMA")

    def test_op_dot(self):
        self.assertEqual(Lexer(".").getNextToken().type, "DOT")

    def test_op_not(self):
        self.assertEqual(Lexer("!").getNextToken().type, "NOT")

    def test_op_minus(self):
        self.assertEqual(Lexer("-").getNextToken().type, "MINUS")

    def test_op_plus(self):
        self.assertEqual(Lexer("+").getNextToken().type, "PLUS")

    def test_op_mult(self):
        self.assertEqual(Lexer("*").getNextToken().type, "MULT")

    def test_op_div(self):
        self.assertEqual(Lexer("/").getNextToken().type, "DIV")

    def test_op_modulo(self):
        self.assertEqual(Lexer("%").getNextToken().type, "MODULO")

    def test_op_less_than(self):
        self.assertEqual(Lexer("<").getNextToken().type, "LESS_THAN")

    def test_op_more_than(self):
        self.assertEqual(Lexer(">").getNextToken().type, "MORE_THAN")

    def test_op_ellipsis(self):
        self.assertEqual(Lexer("...").getNextToken().type, "ELLIPSIS")

    def test_op_inc(self):
        self.assertEqual(Lexer("++").getNextToken().type, "INC")

    def test_op_dec(self):
        self.assertEqual(Lexer("--").getNextToken().type, "DEC")

    def test_op_ptr(self):
        self.assertEqual(Lexer("->").getNextToken().type, "PTR")

    def test_op_and(self):
        self.assertEqual(Lexer("&&").getNextToken().type, "AND")

    def test_op_or(self):
        self.assertEqual(Lexer("||").getNextToken().type, "OR")

    def test_op_bwise_xor(self):
        self.assertEqual(Lexer("^").getNextToken().type, "BWISE_XOR")

    def test_op_bwise_or(self):
        self.assertEqual(Lexer("|").getNextToken().type, "BWISE_OR")

    def test_op_bwise_not(self):
        self.assertEqual(Lexer("~").getNextToken().type, "BWISE_NOT")

    def test_op_bwise_and(self):
        self.assertEqual(Lexer("&").getNextToken().type, "BWISE_AND")

    def test_op_right_shift(self):
        self.assertEqual(Lexer(">>").getNextToken().type, "RIGHT_SHIFT")

    def test_op_left_shift(self):
        self.assertEqual(Lexer("<<").getNextToken().type, "LEFT_SHIFT")

    def test_op_tern_condition(self):
        self.assertEqual(Lexer("?").getNextToken().type, "TERN_CONDITION")

    if __name__ == '__main__':
        unittest.main()
