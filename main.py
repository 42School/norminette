from lexer import Lexer
import sys, glob

verbose = True



def main():
    args = sys.argv
    args.pop(0)

    if '-v' in args:
        verbose = True
        args.pop(args.index('-v'))

    if args == []:
        args = glob.glob("**/*.[ch]", recursive=True)

    for arg in args:
        if arg[-2:] not in [".c", ".h"]:
            print(f"{arg} is not valid C or C header file")
        else:
            print(f"\"{arg}\": OK!")



if __name__ == "__main__":
    main()
