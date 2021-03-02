import sys
import glob
import os
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
import argparse
import pkg_resources
from lexer import Lexer, TokenError
from exceptions import CParsingError
from registry import Registry
from context import Context
from tools.colors import colors
import _thread
from threading import Thread, Event
from multiprocessing import Process, Queue
import time
#import sentry_sdk
#from sentry_sdk import configure_scope
from version import __version__

has_err = False

def timeout(e, timeval=5):
    time.sleep(timeval)
    if e.is_set():
        return
    #sentry_sdk.capture_exception(Exception(TimeoutError))
    _thread.interrupt_main()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="File(s) or folder(s) you wanna run the parser on. If no file provided, runs on current folder.", default=[], action='append', nargs='*')
    parser.add_argument("-d", "--debug", action="count", help="Debug output (multiple values available)", default=0)
    parser.add_argument('-v', '--version', action='version', version='norminette ' + str(__version__))
    #parser.add_argument('-s', '--sentry', action='store_true', default=False)
    parser.add_argument('--cfile', action='store', help="Store C file content directly instead of filename")
    parser.add_argument('--hfile', action='store', help="Store header file content directly instead of filename")
    args = parser.parse_args()
    registry = Registry()
    targets = []
    has_err = None
    content = None

    debug = args.debug
    #if args.sentry == True:
        #sentry_sdk.init("https://e67d9ba802fe430bab932d7b11c9b028@sentry.42.fr/72")
    if args.cfile != None or args.hfile != None:
        targets = ['file.c'] if args.cfile else ['file.h']
        content = args.cfile if args.cfile else args.hfile
    else:
        args.file = args.file[0]
        if args.file == [[]] or args.file == []:
            targets = glob.glob("**/*.[ch]", recursive=True)
            target = targets.sort()
        else:
            for arg in args.file:
                if os.path.exists(arg) is False:
                    print(f"'{arg}' no such file or directory")
                elif os.path.isdir(arg):
                    if arg[-1] != '/':
                        arg = arg + '/'
                    targets.extend(glob.glob(arg + '**/*.[ch]', recursive=True))
                elif os.path.isfile(arg):
                    targets.append(arg)
    event = []
    for target in targets:
        if target[-2:] not in [".c", ".h"]:
            print(f"{target} is not valid C or C header file")
        else:
            #with configure_scope() as scope:
            #    scope.set_extra("File", target)
            try:
                event.append(Event())
                #if args.sentry == True:
                #    proc = Thread(target=timeout, args=(event[-1], 5, ))
                #    proc.daemon = True
                #    proc.start()
                if content == None:
                    with open(target) as f:
                        #print ("Running on", target)
                        source = f.read()
                else:
                    source = content
                lexer = Lexer(source)
                tokens = lexer.get_tokens()
                context = Context(target, tokens, debug)
                registry.run(context, source)
                event[-1].set()
                if context.errors:
                    has_err = True
            # except (TokenError, CParsingError) as e:
            except TokenError as e:
                has_err = True
                print(target + f": KO!\n\t{colors(e.msg, 'red')}")
                event[-1].set()
            except CParsingError as e:
                has_err = True
                print(target + f": KO!\n\t{colors(e.msg, 'red')}")
                event[-1].set()
            except KeyboardInterrupt as e:
                event[-1].set()
                sys.exit(1)
    sys.exit(1 if has_err else 0)

if __name__ == "__main__":
    main()