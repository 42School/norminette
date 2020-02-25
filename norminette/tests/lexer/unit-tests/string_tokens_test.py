import unittest
import sys
from lexer.lexer import Lexer


class StringTokenTest(unittest.TestCase):

    def test_basic_string(self):
        self.assertEqual(
            Lexer('"Basic string"').get_next_token().test(),
            '<STRING="Basic string">')

    def test_basic_L_string(self):
        self.assertEqual(
              Lexer('L"Basic string"').get_next_token().test(),
              '<STRING=L"Basic string">')

    def test_basic_escaped_string(self):
        self.assertEqual(
              Lexer('"Basic \\"string\\""').get_next_token().test(),
              '<STRING="Basic \\"string\\"">')

    def test_escaped_string(self):
        self.assertEqual(
              Lexer('"Escaped \\\\\\"string\\\\\\\\\\\"\\\\"').get_next_token()
              .test(),
              '<STRING="Escaped \\\\\\"string\\\\\\\\\\\"\\\\">')


if __name__ == '__main__':
    unittest.main()
