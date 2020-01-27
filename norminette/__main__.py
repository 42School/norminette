import sys
import glob
from lexer import Lexer, TokenError
from registry import Registry
from context import Context
from tools.colors import format_output as txtformat


def main():
    args = sys.argv
    args.pop(0)
    registry = Registry()

    if args == []:
        args = glob.glob("**/*.[ch]", recursive=True)

    for arg in args:
        if arg[-2:] not in [".c", ".h"]:
            print(f"{arg} is not valid C or C header file")

        else:

            with open(arg) as f:
                try:
                    source = f.read()
                    tokens = Lexer(source).getTokens()
                    context = Context(arg, tokens)
                    registry.run(context)
                except TokenError as e:
                    print(arg + f": KO!\n\t{txtformat(e.msg, 'red')}")


if __name__ == "__main__":
    main()
