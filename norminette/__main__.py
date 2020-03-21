import sys
import glob
import os
from lexer import Lexer, TokenError
from registry import Registry
from context import Context
from tools.colors import colors




def main():
    args = sys.argv
    args.pop(0)
    registry = Registry()
    targets = []
    debug = False

    for arg in args:
        if arg == "-D":
            debug = True
            args.pop(args.index("-D"))
        elif os.path.exists(arg) is False:
            print(f"'{arg}' no such file or directory")
        elif os.path.isdir(arg):
            if arg[-1] != '/':
                arg = arg + '/'
            targets.extend(glob.glob(arg + '**/*.c', recursive=True))
        elif os.path.isfile(arg):
            targets.append(arg)

    if args == []:
        targets = glob.glob("**/*.[ch]", recursive=True)
        target = targets.sort()

    for target in targets:
        if target[-2:] not in [".c", ".h"]:
            print(f"{arg} is not valid C or C header file")

        else:
            with open(target) as f:
                try:
                    source = f.read()
                    lexer = Lexer(source)
                    tokens = lexer.get_tokens()
                    context = Context(target, tokens, debug)
                    registry.run(context)
                except TokenError as e:
                    print(target + f": KO!\n\t{colors(e.msg, 'red')}")


if __name__ == "__main__":
    main()
