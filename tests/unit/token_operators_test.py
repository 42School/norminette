import unittest
import sys
sys.path.append('../..')
from lexer import Lexer

class TokenOperatorsTest(unittest.TestCase):

  def  test_op_right_assign(self):
    lex = Lexer(">>=")
    self.assertEqual(lex.getNextToken().type, "OP_RIGHT_ASSIGN")

  def  test_op_left_assign(self):
    lex = Lexer("<<=")
    self.assertEqual(lex.getNextToken().type, "OP_LEFT_ASSIGN")

  def  test_op_add_assign(self):
    lex = Lexer("+=")
    self.assertEqual(lex.getNextToken().type, "OP_ADD_ASSIGN")

  def  test_op_sub_assign(self):
    lex = Lexer("-=")
    self.assertEqual(lex.getNextToken().type, "OP_SUB_ASSIGN")

  def  test_op_mul_assign(self):
    lex = Lexer("*=")
    self.assertEqual(lex.getNextToken().type, "OP_MUL_ASSIGN")

  def  test_op_div_assign(self):
    lex = Lexer("/=")
    self.assertEqual(lex.getNextToken().type, "OP_DIV_ASSIGN")

  def  test_op_mod_assign(self):
    lex = Lexer("%=")
    self.assertEqual(lex.getNextToken().type, "OP_MOD_ASSIGN")

  def  test_op_and_assign(self):
    lex = Lexer("&=")
    self.assertEqual(lex.getNextToken().type, "OP_AND_ASSIGN")

  def  test_op_xor_assign(self):
    lex = Lexer("^=")
    self.assertEqual(lex.getNextToken().type, "OP_XOR_ASSIGN")

  def  test_op_or_assign(self):
    lex = Lexer("|=")
    self.assertEqual(lex.getNextToken().type, "OP_OR_ASSIGN")

  def  test_op_le_assign(self):
    lex = Lexer("<=")
    self.assertEqual(lex.getNextToken().type, "OP_LE")

  def  test_op_ge_assign(self):
    lex = Lexer(">=")
    self.assertEqual(lex.getNextToken().type, "OP_GE")

  def  test_op_eq_assign(self):
    lex = Lexer("==")
    self.assertEqual(lex.getNextToken().type, "OP_EQ")

  def  test_op_ne_assign(self):
    lex = Lexer("!=")
    self.assertEqual(lex.getNextToken().type, "OP_NE")

  def  test_op_assign(self):
    lex = Lexer("=")
    self.assertEqual(lex.getNextToken().type, "OP_ASSIGN")

  def  test_op_semi_colon(self):
    lex = Lexer(";")
    self.assertEqual(lex.getNextToken().type, "OP_SEMI_COLON")

  def  test_op_colon(self):
    lex = Lexer(":")
    self.assertEqual(lex.getNextToken().type, "OP_COLON")

  def  test_op_comma(self):
    lex = Lexer(",")
    self.assertEqual(lex.getNextToken().type, "OP_COMMA")

  def  test_op_dot(self):
    lex = Lexer(".")
    self.assertEqual(lex.getNextToken().type, "OP_DOT")

  def  test_op_not(self):
    lex = Lexer("!")
    self.assertEqual(lex.getNextToken().type, "OP_NOT")

  def  test_op_minus(self):
    lex = Lexer("-")
    self.assertEqual(lex.getNextToken().type, "OP_MINUS")

  def  test_op_plus(self):
    lex = Lexer("+")
    self.assertEqual(lex.getNextToken().type, "OP_PLUS")

  def  test_op_mult(self):
    lex = Lexer("*")
    self.assertEqual(lex.getNextToken().type, "OP_MULT")

  def  test_op_div(self):
    lex = Lexer("/")
    self.assertEqual(lex.getNextToken().type, "OP_DIV")

  def  test_op_modulo(self):
    lex = Lexer("%")
    self.assertEqual(lex.getNextToken().type, "OP_MODULO")

  def  test_op_less_than(self):
    lex = Lexer("<")
    self.assertEqual(lex.getNextToken().type, "OP_LESS_THAN")

  def  test_op_more_than(self):
    lex = Lexer(">")
    self.assertEqual(lex.getNextToken().type, "OP_MORE_THAN")

  def  test_op_ellipsis(self):
    lex = Lexer("...")
    self.assertEqual(lex.getNextToken().type, "OP_ELLIPSIS")

  def  test_op_inc(self):
    lex = Lexer("++")
    self.assertEqual(lex.getNextToken().type, "OP_INC")

  def  test_op_dec(self):
    lex = Lexer("--")
    self.assertEqual(lex.getNextToken().type, "OP_DEC")

  def  test_op_ptr(self):
    lex = Lexer("->")
    self.assertEqual(lex.getNextToken().type, "OP_PTR")

  def  test_op_and(self):
    lex = Lexer("&&")
    self.assertEqual(lex.getNextToken().type, "OP_AND")

  def  test_op_or(self):
    lex = Lexer("||")
    self.assertEqual(lex.getNextToken().type, "OP_OR")

  def  test_op_bwise_xor(self):
    lex = Lexer("^")
    self.assertEqual(lex.getNextToken().type, "OP_BWISE_XOR")

  def  test_op_bwise_or(self):
    lex = Lexer("|")
    self.assertEqual(lex.getNextToken().type, "OP_BWISE_OR")

  def  test_op_bwise_not(self):
    lex = Lexer("~")
    self.assertEqual(lex.getNextToken().type, "OP_BWISE_NOT")

  def  test_op_bwise_and(self):
    lex = Lexer("&")
    self.assertEqual(lex.getNextToken().type, "OP_BWISE_AND")

  def  test_op_right_shift(self):
    lex = Lexer(">>")
    self.assertEqual(lex.getNextToken().type, "OP_RIGHT_SHIFT")

  def  test_op_left_shift(self):
    lex = Lexer("<<")
    self.assertEqual(lex.getNextToken().type, "OP_LEFT_SHIFT")

  def  test_op_tern_condition(self):
    lex = Lexer("?")
    self.assertEqual(lex.getNextToken().type, "OP_TERN_CONDITION")


if __name__ == '__main__':
    unittest.main()
