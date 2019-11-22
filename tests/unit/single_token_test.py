import unittest
import sys
sys.path.append('../..')
from lexer import Lexer
from dictionary import keywords, operators, brackets

for key, value in keywords.items():
  print(key + "=>" + value)

class SingleTokenTest(unittest.TestCase):

  def test_single_token(self):
    for key, value in keywords.items():
      self.assertEqual(Lexer(key).getNextToken().type, value)



if __name__ == '__main__':
    unittest.main()