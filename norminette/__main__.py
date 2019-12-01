import sys
import glob
from lexer.lexer import Lexer, TokenError


def main():
    args = sys.argv
    args.pop(0)

    if args == []:
        args = glob.glob("**/*.[ch]", recursive=True)

    for arg in args:
        if arg[-2:] not in [".c", ".h"]:
            print(f"{arg} is not valid C or C header file")
        else:
            with open(arg) as f:
                try:
                    Lexer(f.read()).getTokens()
                    print(arg + ": OK")
                except TokenError:
                    print(arg + ": KO")


if __name__ == "__main__":
    main()
