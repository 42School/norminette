from norm_error import NormError
from lexer.dictionary import operators, brackets
from tools.colors import colors
from scope import *
from exceptions import CParsingError

type_specifiers = [
    "CHAR",
    "DOUBLE",
    "ENUM",
    "FLOAT",
    "INT",
    "UNION",
    "VOID",
]

misc_specifiers = [
    "CONST",
    "REGISTER",
    "STATIC",
    "VOLATILE"
]

size_specifiers = [
    "LONG",
    "SHORT"
]

sign_specifiers = [
    "SIGNED",
    "UNSIGNED"
]

whitespaces = [
    "SPACE",
    "TAB",
    "NEWLINE"
]

arg_separator = [
    "COMMA",
    "CLOSING_PARENTHESIS"
]


class Context:
    def __init__(self, filename, tokens, debug=False):
        # File relative informations
        self.filename = filename
        self.filetype = filename.split('.')[-1]  # ?
        self.tokens = tokens
        self.debug = debug

        # Rule relative informations
        self.history = []
        self.errors = []
        self.tkn_scope = len(tokens)

        # Scope informations
        self.scope = GlobalScope()
        self.sub = None
        self.fname_pos = 0
        self.arg_pos = [0, 0]

        # Preprocessor handling
        self.preproc_scope_indent = 0

    def peek_token(self, pos):
        return self.tokens[pos] if pos < len(self.tokens) else None

    def pop_tokens(self, stop):
        self.tokens = self.tokens[stop:]

    def check_token(self, pos, value):
        """Compares the token at 'pos' against a value or list of values
        """
        tkn = self.peek_token(pos)

        if tkn is None:
            return False

        if isinstance(value, list):
            if tkn.type in value:
                return True
            return False

        return tkn.type == value

    def new_error(self, errno, tkn):
        self.errors.append(NormError(errno, tkn.pos[0], tkn.pos[1]))

    def get_parent_rule(self):
        if len(self.history) == 0:
            return ""
        return self.history[-1 if len(self.history) == 1 else -2]

    def update(self):
        """Updates the scope if needed after a primary rule has succeeded
        """
        if self.sub is not None:
            self.scope = self.sub
            self.sub = None

        elif type(self.scope) is ControlStructure:

            if self.scope.multiline is False:
                if self.scope.lines > 0:
                    self.scope = self.scope.outer()
                    self.sub = None
                    self.update()

    def dprint(self, rule, pos):
        """Debug printing, shows the primary rules that succeed in matching
            tokens and print the matching tokens
        """
        if self.debug is False:
            return
        print(f"{colors(self.filename, 'cyan')} - {colors(rule, 'green')} \
In \"{self.scope.name}\" from \
\"{self.scope.parent.name if self.scope.parent is not  None else None}\":")
        i = 0
        for t in self.tokens[:pos]:
            if i == 0:
                print("\t\t", end="")
            if t.type == "NEWLINE":
                print(t)
                i = 0
            else:
                print(t, end=" ")
                i += 1
        if self.tokens[pos - 1].type != "NEWLINE":
            print("")

    def eol(self, pos):
        """Skips white space characters (tab, space) until end of line
            (included) or any other token (excluded)
        """
        while self.check_token(pos, ["TAB", "SPACE", "NEWLINE"]) is True:
            if self.check_token(pos, "NEWLINE"):
                pos += 1
                break
            pos += 1
        return pos

    def skip_ws(self, pos):
        while self.check_token(pos, ["TAB", "SPACE", "NEWLINE"]):
            pos += 1
        return pos

    def skip_nest(self, pos):
        """Skips anything between two brackets, parentheses or braces starting
            at 'pos', if the brackets, parentheses or braces are not closed or
            are closed in the wrong order an error shall be raised
        """
        lbrackets = ["LBRACKET", "LBRACE", "LPARENTHESIS"]
        rbrackets = ["RBRACKET", "RBRACE", "RPARENTHESIS"]
        c = self.peek_token(pos).type
        if c not in lbrackets:
            return pos
        c = rbrackets[lbrackets.index(c)]
        i = pos + 1
        while self.peek_token(i) is not None:
            if self.check_token(i, lbrackets) is True:
                i = self.skip_nest(i)
                if i == -1:
                    return -1
            elif self.check_token(i, rbrackets) is True:
                if c == self.peek_token(i).type:
                    return i
                raise CParsingError("Nested parentheses, braces or brackets\
 are not correctly closed")

            i += 1
        return -1

    def skip_misc_specifier(self, pos):
        i = self.skip_ws(pos)
        if self.check_token(i, misc_specifiers):
            i += 1
            i = self.skip_ws(i)
        return i

    def check_type_specifier(self, pos):
        """Returns True if the tokens starting at 'pos' could match a valid
            type specifier. Valid type specifiers consist of:
                -an optionnal 'misc' specifier (const, register, volatile ...)
                -an optionnal size specifier (long or short)
                -a type specifier (int, char, double, etc...)
                    OR an IDENTIFIER
                    OR a user type specifier (struct, union, enum) + IDENTIFIER
        """
        i = self.skip_misc_specifier(pos)

        if self.check_token(i, sign_specifiers):
            i += 1
            i = self.skip_misc_specifier(i)
            if self.check_token(i, size_specifiers):
                i += 1
                i = self.skip_misc_specifier(i)
                if self.check_token(i, type_specifiers):
                    i += 1
                    i = self.skip_misc_specifier(i)
                    return True, i
                return True, i
            return True, i

        if self.check_token(i, size_specifiers):
            i += 1
            i = self.skip_misc_specifier(i)
            if self.check_token(i, type_specifiers):
                i += 1
                i = self.skip_misc_specifier(i)
                return True, i
            return True, i

        if self.check_token(i, ["STRUCT", "ENUM", "UNION"]):
            i += 1
            i = self.skip_misc_specifier(i)
            if self.check_token(i, "IDENTIFIER"):
                i += 1
                return True, i
            return False, 0

        if self.check_token(i, type_specifiers + ["IDENTIFIER"]):
            i += 1
            i = self.skip_misc_specifier(i)
            return True, i

        return False, pos

    def check_identifier(self, pos):
        i = pos
        while self.check_token(i, whitespaces + ["MULT"]):
            i += 1
        if self.check_token(i, "IDENTIFIER"):
            return True, i
        return False, pos
