import sys
import glob
import difflib
from functools import wraps
from lexer import Lexer
from lexer import TokenError


def read_file(filename):
    with open(filename) as f:
        return f.read()


class norminetteFileTester():

    def __init__(self):
        self.__tests = 0
        self.__failed = 0
        self.__success = 0
        self.result = []

    def assertEqual(self, first, second):
        self.maxDiff = None
        if first == second:
            self.__success += 1
            print("OK")
            self.result.append(".")
        else:
            print("KO")
            self.__failed += 1
            diff = difflib.ndiff(first.splitlines(keepends=True),
                                 second.splitlines(keepends=True))
            diff = list(diff)
            self.result.append("x")
            print(''.join(diff))

    def assertRaises(self, test, ref):
        try:
            test()
            self.__failed += 1
            print("KO")
            self.result.append("x")
        except TokenError as e:
            if e.err == ref:
                self.__success += 1
                print("OK")
                self.result.append(".")
            else:
                print("KO")
                print(e.err + "(output)\n", ref + "(reference output)")
                self.__failed += 1
                self.result.append("x")

    def test_files(self):
        files = glob.glob("tests/files/*.c")
        failing_tests = glob.glob("tests/files/*.error")
        files.sort()
        for f in files:
            self.__tests += 1
            print(f.split('/')[-1], end=": ")
            if f.split('/')[-1].startswith("ok"):
                output = Lexer(read_file(f)).checkTokens()
                reference_output = read_file(f.split(".")[0] + ".tokens")
                self.assertEqual(output, reference_output)
            elif f.split('/')[-1].startswith("ko"):
                reference_output = read_file(f.split(".")[0] + ".err")
                func = Lexer(read_file(f)).checkTokens
                self.assertRaises(func, reference_output)
        print("----------------------------------")
        print(f'Total {self.__tests}\nSuccess {self.__success}' +
              f', Failed {self.__failed}:')
        print("".join(self.result))
        print("OK!" if self.__failed == 0 else "KO!")
        sys.exit(0 if self.__failed == 0 else 1)


if __name__ == '__main__':
    norminetteFileTester().test_files()
