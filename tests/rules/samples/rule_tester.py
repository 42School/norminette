import difflib
import glob
import sys
from io import StringIO

from norminette.context import Context
from norminette.lexer import Lexer
from registry import Registry


registry = Registry()


def read_file(filename):
    with open(filename) as f:
        return f.read()


class norminetteRuleTester:
    def __init__(self):
        self.__tests = 0
        self.__failed = 0
        self.__success = 0
        self.result = []

    def assertEqual(self, test, ref):
        if test == ref:
            self.__success += 1
            print("OK")
            self.result.append("✓ ")
        else:
            self.__failed += 1
            print("Error")
            diff = difflib.ndiff(
                test.splitlines(keepends=True), ref.splitlines(keepends=True)
            )
            diff = list(diff)
            self.result.append("✗ ")
            print("".join(diff))

    def test_file(self, filename):
        stdout = sys.stdout
        sys.stdout = buff = StringIO()
        lexer = Lexer(read_file(filename))
        context = Context(filename.split("/")[-1], lexer.get_tokens(), debug=2)
        registry.run(context, read_file(filename))
        reference_output = read_file(filename.split(".")[0] + ".out")
        sys.stdout = stdout
        self.assertEqual(buff.getvalue(), reference_output)

    def run_tests(self):
        files = glob.glob("tests/rules/*.[ch]")
        files.sort()
        for f in files:
            self.__tests += 1
            print("TESTER -", f.split("/")[-1], end=": ")
            try:
                self.test_file(f)
            except Exception as e:
                self.__failed += 1
                print("Error")
                print(e)
                self.result.append("✗ ")
                continue
        print("----------------------------------")
        print(f"Total {self.__tests}")
        print("".join(self.result))
        print(f"Success {self.__success}, Failed {self.__failed}: ", end="")
        print("✅ OK!" if self.__failed == 0 else "❌ Error!")

        sys.exit(0 if self.__failed == 0 else 1)


if __name__ == "__main__":
    norminetteRuleTester().run_tests()
