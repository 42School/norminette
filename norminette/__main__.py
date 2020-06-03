import sys
import glob
import os
from lexer import Lexer, TokenError
from exceptions import CParsingError
from registry import Registry
from context import Context
from tools.colors import colors
# import sentry_sdk


# sentry_sdk.init("https://e67d9ba802fe430bab932d7b11c9b028@sentry.42.fr/72")


has_err = False

def main():
    args = sys.argv
    args.pop(0)
    registry = Registry()
    targets = []
    debug = False

    # This here should be change to use argparse module I think
    for arg in args:
        if arg == "-D":
            debug = True
            if args == [arg]:
                args = []
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
                    registry.run(context, source)
                    if context.errors is not []:
                        has_err = True
                # except (TokenError, CParsingError) as e:
                except TokenError as e:
                    has_err = True
                    print(target + f": KO!\n\t{colors(e.msg, 'red')}")
                except CParsingError as e:
                    has_err = True
                    print(target + f": KO!\n\t{colors(e.msg, 'red')}")

    sys.exit(1 if has_err else 0)

if __name__ == "__main__":
    main()