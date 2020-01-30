import sys
import glob
import os
from lexer import Lexer, TokenError
from registry import Registry
from context import Context
from tools.colors import format_output as txtformat


def main():
    args = sys.argv
    args.pop(0)
    registry = Registry()
    targets = []

    for arg in args:
        if os.path.isdir(arg):
            if arg[-1] != '/':
                arg = arg + '/'
            targets.extend(glob.glob(arg + '**/*.c', recursive=True))

        elif os.path.isfile(arg):
            targets.append(arg)

    if args == []:
        targets = glob.glob("**/*.[ch]", recursive=True)

    for target in targets:
        if target[-2:] not in [".c", ".h"]:
            print(f"{arg} is not valid C or C header file")

        else:
            with open(target) as f:
                try:
                    source = f.read()
                    tokens = Lexer(source).getTokens()
                    context = Context(target, tokens)
                    registry.run(context)
                except TokenError as e:
                    print(target + f": KO!\n\t{txtformat(e.msg, 'red')}")


if __name__ == "__main__":
    main()
