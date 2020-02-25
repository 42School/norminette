import unittest
import glob
import difflib
from lexer import Lexer


def test_file(filename):
    pass


class norminetteFileTester():

    def __init__(self):
        self.__tests = 0
        self.__failed = 0
        self.__success = 0
        self.result = []

    def assertEqual(self, test, ref):
        self.maxDiff
        if test == ref:
            self.__success += 1
            print("OK")
            self.result.append("✓ ")
        else:
            self.__failed += 1
            print("KO")
            diff = difflib.ndiff(test.splitlines(keepends=True),
                                 ref.splitlines(keepends=True))
            diff = list(diff)
            self.result.append("✗ ")
            print(''.join(diff))

    def run_tests(self):
        files = glob.glob("tests/rules/files/*.c")
        files.sort()
        for f in files:
            self.__tests += 1
            print(f.split('/')[-1], end=": ")
            try:
                output = Lexer(read_file(f)).check_tokens()
            except TokenError as t:
                self.__failed += 1
                print("KO")
                print(t)
                self.result.append("✗ ")
                continue
            reference_output = read_file(f.split(".")[0] + ".tokens")
            self.assertEqual(output, reference_output)
