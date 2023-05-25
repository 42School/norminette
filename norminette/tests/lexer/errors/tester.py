import difflib
import sys

from norminette.lexer import Lexer
from norminette.lexer import TokenError
from tests.lexer.errors.dict import failed_tokens_tests as test_dict


def read_file(filename):
    with open(filename) as f:
        return f.read()


class norminetteTester:
    def __init__(self):
        self.__tests = 0
        self.__failed = 0
        self.__success = 0
        self.result = []

    def assertRaises(self, test, ref, test_line):
        try:
            diff = "".join(test())
            self.__failed += 1
            print(test_line + "Error")
            print(diff, end="")
            self.result.append("✗ ")
        except TokenError as e:
            if e.msg == ref:
                self.__success += 1
                self.result.append("✓ ")
            else:
                self.__failed += 1
                print(test_line + "Error")
                diff = difflib.ndiff(e.msg.splitlines(), ref.splitlines())
                diff = list(diff)
                self.result.append("✗ ")
                print("".join(diff))

    def main(self):
        print("\n\nTesting error cases:\n")
        i = 1
        for key, val in test_dict.items():
            self.__tests += 1
            ref_output = f"Error: Unrecognized token line {val[0]}, col {val[1]}"
            func = Lexer(key).check_tokens
            self.assertRaises(func, ref_output, f"Test {i}: " + repr(str(key)))
            i += 1

        print("----------------------------------")
        print(f"Total {self.__tests}")
        print("".join(self.result))
        print(f"Success {self.__success}, Failed {self.__failed}: ", end="")
        print("✅ OK!" if self.__failed == 0 else "❌ Error!")

        sys.exit(0 if self.__failed == 0 else 1)


if __name__ == "__main__":
    norminetteTester().main()
