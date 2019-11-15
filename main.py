from lexer import Lexer
import sys

verbose = True



def main():
    args = sys.argv
    args.pop(0)

    if '-v' in args:
        verbose = True
        args.pop(args.index('-v'))

    for arg in args:
        print(arg)



if __name__ == "__main__":
    main()
