import unittest
import sys
import glob
from functools import wraps
from lexer import Lexer, TokenError


def read_file(filename):
    with open(filename) as f:
        return f.read()


class norminetteFileTester(unittest.TestCase):
    def assertEqual(self, first, second):
        self.maxDiff = None
        try:
            super().assertEqual(first, second)
            print("OK")
        except TokenError as t:
            print("KO")

    def assertRaises(self, test):
        try:
            test()
            print("KO")
            return False
        except TokenError:
            print("OK")
            return True

    def test_files(self):
        files = glob.glob("tests/files/*.c")
        failing_tests = glob.glob("tests/files/*.error")
        for f in files:
            if f.split('/')[-1].startswith("ok"):
                print(f.split('/')[-1], end=": ")
                output = Lexer(read_file(f)).checkTokens()
                reference_output = read_file(f.split(".")[0] + ".tokens")
                self.assertEqual(output, reference_output)
            elif f.split('/')[-1].startswith("ko"):
                print(f.split('/')[-1], end=": ")
                self.assertRaises(Lexer(read_file(f)).checkTokens)
                continue


if __name__ == '__main__':
    unittest.main()
