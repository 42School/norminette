import unittest
import sys
sys.path.append('../..')
from lexer import Lexer

class ConstantTokensTest(unittest.TestCase):

  def test_basic_constant(self):
    self.assertEqual(Lexer("42").getNextToken().test(), "<NUM_CONSTANT=42>")

  def test_float_constant(self):
    self.assertEqual(Lexer("4.2").getNextToken().test(), "<NUM_CONSTANT=4.2>")

  def test_float_constant_starting_with_dot(self):
    self.assertEqual(Lexer(".42").getNextToken().test(), "<NUM_CONSTANT=.42>")

  def test_double_constant(self):
    self.assertEqual(Lexer("4e2").getNextToken().test(), "<NUM_CONSTANT=4e2>")

  def test_double_constant_starting_with_dot(self):
    self.assertEqual(Lexer(".4e2").getNextToken().test(), "<NUM_CONSTANT=.4e2>")

if __name__ == '__main__':
    unittest.main()
