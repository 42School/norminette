import difflib
import glob
import sys

from norminette.lexer import Lexer
from norminette.lexer import TokenError


def read_file(filename):
    with open(filename) as f:
        return f.read()


class norminetteFileTester:
    def __init__(self):
        self.__tests = 0
        self.__failed = 0
        self.__success = 0
        self.result = []

    def assertEqual(self, first, second):
        if first == second:
            self.__success += 1
            print("OK")
            self.result.append("✓ ")
        else:
            print("Error")
            self.__failed += 1
            diff = difflib.ndiff(
                first.splitlines(keepends=True), second.splitlines(keepends=True)
            )
            diff = list(diff)
            self.result.append("✗ ")
            print("".join(diff))

    def assertRaises(self, test, ref):
        try:
            diff = "".join(test())
            self.__failed += 1
            print("Error")
            print(diff, end="")
            self.result.append("✗ ")
        except TokenError as e:
            if e.msg == ref:
                self.__success += 1
                print("OK")
                self.result.append("✓ ")
            else:
                self.__failed += 1
                print("Error")
                diff = difflib.ndiff(e.msg.splitlines(), ref.splitlines())
                diff = list(diff)
                self.result.append("✗ ")
                print("".join(diff))

    def test_files(self):
        files = glob.glob("tests/lexer/files/*.c")
        files.sort()
        for f in files:
            self.__tests += 1
            print(f.split("/")[-1], end=": ")

            try:
                output = Lexer(read_file(f)).check_tokens()
            except TokenError as t:
                self.__failed += 1
                print("Error")
                print(t)
                self.result.append("✗ ")
                continue
            reference_output = read_file(f.split(".")[0] + ".tokens")
            self.assertEqual(output, reference_output)

        print("----------------------------------")
        print(f"Total {self.__tests}")
        print("".join(self.result))
        print(f"Success {self.__success}, Failed {self.__failed}: ", end="")
        print("✅ OK!" if self.__failed == 0 else "❌ Error!")

        sys.exit(0 if self.__failed == 0 else 1)


if __name__ == "__main__":
    norminetteFileTester().test_files()
