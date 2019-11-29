import unittest
import sys
import glob
from functools import wraps
from lexer import Lexer


def read_file(filename):
    with open(filename) as f:
        return f.read()


class norminetteFileTester(unittest.TestCase):
    def assertEqual(self, first, second):
        self.maxDiff = None
        try:
            super().assertEqual(first, second)
            print("ok")
        except Exception as e:
            print(e)

    def test_files(self):
        files = glob.glob("tests/files/*.c")
        for f in files:
            print(f, end=": ")
            output = Lexer(read_file(f)).checkTokens()
            reference_output = read_file(f.split(".")[0] + ".tokens")
            self.assertEqual(output, reference_output)


if __name__ == '__main__':
    unittest.main()
