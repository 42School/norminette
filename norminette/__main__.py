import glob
import os
import sys

import argparse
from norminette.lexer import Lexer, TokenError
from norminette.exceptions import CParsingError
from norminette.registry import Registry
from norminette.context import Context
from norminette.tools.colors import colors
from norminette import __version__

import _thread
from threading import Event
import time


has_err = False


def timeout(e, timeval=5):
    time.sleep(timeval)
    if e.is_set():
        return
    _thread.interrupt_main()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file",
        help="File(s) or folder(s) you wanna run the parser on. If no file provided, runs on current folder.",
        default=[],
        action="append",
        nargs="*",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="count",
        help="Debug output (multiple values available)",
        default=0,
    )
    parser.add_argument(
        "-o",
        "--only-filename",
        action="store_true",
        help="By default norminette displays the full path to the file, this allows to show only filename",
        default=False,
    )
    parser.add_argument("-v", "--version", action="version", version="norminette " + str(__version__))
    parser.add_argument(
        "--cfile",
        action="store",
        help="Store C file content directly instead of filename",
    )
    parser.add_argument(
        "--hfile",
        action="store",
        help="Store header file content directly instead of filename",
    )
    parser.add_argument("-R", nargs=1, help="compatibility for norminette 2")
    args = parser.parse_args()
    registry = Registry()
    targets = []
    has_err = None
    content = None

    debug = args.debug
    if args.cfile != None or args.hfile != None:
        targets = ["file.c"] if args.cfile else ["file.h"]
        content = args.cfile if args.cfile else args.hfile
    else:
        args.file = args.file[0]
        if args.file == [[]] or args.file == []:
            targets = glob.glob("**/*.[ch]", recursive=True)
        else:
            for arg in args.file:
                if os.path.exists(arg) is False:
                    print(f"'{arg}' no such file or directory")
                elif os.path.isdir(arg):
                    if arg[-1] != "/":
                        arg = arg + "/"
                    targets.extend(glob.glob(arg + "**/*.[ch]", recursive=True))
                elif os.path.isfile(arg):
                    targets.append(arg)
    event = []
    for target in targets:
        if target[-2:] not in [".c", ".h"]:
            print(f"Error: {target} is not valid C or C header file")
        else:
            try:
                event.append(Event())
                if content == None:
                    with open(target) as f:
                        source = f.read()
                else:
                    source = content
                lexer = Lexer(source)
                tokens = lexer.get_tokens()
                if args.only_filename == True:
                    target = target.split("/")[-1]
                context = Context(target, tokens, debug, args.R)
                registry.run(context, source)
                event[-1].set()
                if context.errors:
                    has_err = True
            except TokenError as e:
                has_err = True
                print(target + f": Error!\n\t{colors(e.msg, 'red')}")
                event[-1].set()
            except CParsingError as e:
                has_err = True
                print(target + f": Error!\n\t{colors(e.msg, 'red')}")
                event[-1].set()
            except KeyboardInterrupt as e:
                event[-1].set()
                sys.exit(1)
    sys.exit(1 if has_err else 0)


if __name__ == "__main__":
    main()
