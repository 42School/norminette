import glob
import os
import sys
from importlib.metadata import version

import argparse
from norminette.lexer import Lexer, TokenError
from norminette.exceptions import CParsingError
from norminette.registry import Registry
from norminette.context import Context
from norminette.tools.colors import colors

from pathlib import Path

import _thread
from threading import Event
import time
import subprocess


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
        help="Debug output (-dd outputs the whole tokenization and such, used for developping)",
        default=0,
    )
    parser.add_argument(
        "-o",
        "--only-filename",
        action="store_true",
        help="By default norminette displays the full path to the file, this allows to show only filename",
        default=False,
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="norminette " + version("norminette"),
    )
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
    parser.add_argument(
        "--filename",
        action="store",
        help="Stores filename if --cfile or --hfile is passed",
    )
    parser.add_argument(
        "--use-gitignore",
        action="store_true",
        help="Parse only source files not match to .gitignore",
    )
    parser.add_argument("-R", nargs=1, help="compatibility for norminette 2")
    args = parser.parse_args()
    registry = Registry()
    targets = []
    has_err = None
    content = None

    debug = args.debug
    if args.cfile is not None or args.hfile is not None:
        if args.filename:
            targets = [args.filename]
        else:
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

    if args.use_gitignore:
        tmp_targets = []
        for target in targets:
            command = ["git", "check-ignore", "-q", target]
            exit_code = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode
            """
            see: $ man git-check-ignore
            EXIT STATUS
                  0: One or more of the provided paths is ignored.
                  1: None of the provided paths are ignored.
                128: A fatal error was encountered.
            """
            if exit_code == 0:
                pass
            elif exit_code == 1:
                tmp_targets.append(target)
            elif exit_code == 128:
                print(f'Error: something wrong with --use-gitignore option {target}')
                sys.exit(0)
        targets = tmp_targets
    event = []
    for target in filter(os.path.isfile, targets):
        if target[-2:] not in [".c", ".h"]:
            print(f"Error: {target} is not valid C or C header file")
        else:
            try:
                event.append(Event())
                if content is None:
                    with open(target) as f:
                        try:
                            source = f.read()
                        except Exception as e:
                            print("Error: File could not be read: ", e)
                            sys.exit(0)
                else:
                    source = content
                try:
                    lexer = Lexer(source)
                    tokens = lexer.get_tokens()
                except KeyError as e:
                    print("Error while parsing file:", e)
                    sys.exit(0)
                if args.only_filename is True:
                    # target = target.split("/")[-1]
                    target = Path(target).name
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
            except KeyboardInterrupt:
                event[-1].set()
                sys.exit(1)
    sys.exit(1 if has_err else 0)


if __name__ == "__main__":
    main()
