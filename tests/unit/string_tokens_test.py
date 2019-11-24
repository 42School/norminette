
import unittest
import sys
sys.path.append('../..')
from lexer import Lexer

class StringTokenTest(unittest.TestCase):

  def test_basic_string(self):
    self.assertEqual(Lexer('"Basic string"').getNextToken().test(),
                            '<STRING_CONSTANT="Basic string">')

  def test_basic_L_string(self):
    self.assertEqual(Lexer('L"Basic string"').getNextToken().test(),
                            '<STRING_CONSTANT=L"Basic string">')

  def test_basic_escaped_string(self):
    self.assertEqual(Lexer('"Basic \\"string\\""').getNextToken().test(),
                            '<STRING_CONSTANT="Basic \\"string\\"">')

  def test_escaped_string(self):
    self.assertEqual(Lexer('"Escaped \\\\\\"string\\\\\\\\\\"\\\\"').getNextToken().test(),
                            '<STRING_CONSTANT="Escaped \\\\\\"string\\\\\\\\\\\"\\\\">')


if __name__ == '__main__':
    unittest.main()
