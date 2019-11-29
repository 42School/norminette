from lexer import Lexer
import sys
import glob



def main():
    args = sys.argv
    args.pop(0)

    if args == []:
        args = glob.glob("**/*.[ch]", recursive=True)

    for arg in args:
        if arg[-2:] not in [".c", ".h"]:
            print(f"{arg} is not valid C or C header file")
        else:
            print(Lexer.getTokens())


if __name__ == "__main__":
    main()
