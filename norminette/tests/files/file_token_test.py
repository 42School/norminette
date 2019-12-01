import unittest
import sys
import glob
from functools import wraps
from lexer.lexer import Lexer, TokenError


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

    def assertRaises(self, test, ref):
        try:
            test()
            print("KO")
            return False
        except TokenError as e:
            if e.err == ref:
                print("OK")
                return True
            else:
                print("KO")
                return False

    def test_files(self):
        files = glob.glob("tests/files/*.c")
        failing_tests = glob.glob("tests/files/*.error")
        files.sort()
        for f in files:
            print(f.split('/')[-1], end=": ")
            if f.split('/')[-1].startswith("ok"):
                output = Lexer(read_file(f)).checkTokens()
                reference_output = read_file(f.split(".")[0] + ".tokens")
                self.assertEqual(output, reference_output)
            elif f.split('/')[-1].startswith("ko"):
                reference_output = read_file(f.split(".")[0] + ".err")
                func = Lexer(read_file(f)).checkTokens
                self.assertRaises(func, reference_output)


if __name__ == '__main__':
    unittest.main()
