from norm_error import NormError
from lexer.dictionary import operators, brackets
from tools.colors import colors
from scope import *
from exceptions import CParsingError

types = [
    "CHAR",
    "DOUBLE",
    "ENUM",
    "FLOAT",
    "INT",
    "UNION",
    "VOID",
    "LONG",
    "SHORT",
    "SIGNED",
    "UNSIGNED"
]

utypes = [
    "STRUCT",
    "ENUM",
    "UNION"
]

glued_operators = [
    "MINUS",
    "PLUS",
    "MULT",
    "DIV",
    "MODULO",
    "TERN_CONDITION",
    "COMMA",
    "GOTO",
    "LABEL",
    "SWITCH",
    "CASE",
    "LESS_OR_EQUAL",
    "GREATER_OR_EQUAL",
    "EQUALS",
    "NOT_EQUAL",
    "LESS_THAN",
    "MORE_THAN",
    "BWISE_XOR",
    "BWISE_OR",
    "BWISE_NOT",
    "BWISE_AND",
    "RIGHT_SHIFT",
    "LEFT_SHIFT",
    "TERN_CONDITION",
    "ASSIGN",
    "RIGHT_ASSIGN",
    "LEFT_ASSIGN",
    "ADD_ASSIGN",
    "SUB_ASSIGN",
    "MUL_ASSIGN",
    "DIV_ASSIGN",
    "MOD_ASSIGN",
    "AND_ASSIGN",
    "XOR_ASSIGN",
    "OR_ASSIGN",
]

operators = [
    "LESS_OR_EQUAL",
    "GREATER_OR_EQUAL",
    "EQUALS",
    "NOT_EQUAL",
    "ASSIGN",
    "NOT",
    "MINUS",
    "PLUS",
    "MULT",
    "DIV",
    "MODULO",
    "LESS_THAN",
    "MORE_THAN",
    "ELLIPSIS",
    "INC",
    "DEC",
    "PTR",
    "AND",
    "OR",
    "BWISE_XOR",
    "BWISE_OR",
    "BWISE_NOT",
    "BWISE_AND",
    "RIGHT_SHIFT",
    "LEFT_SHIFT",
    "TERN_CONDITION",
    "COMMA",
    "GOTO",
    "LABEL",
    "SWITCH",
    "CASE"
]
misc_specifiers = [
    "CONST",
    "REGISTER",
    "STATIC",
    "VOLATILE",
    "EXTERN",
    "INLINE",
    "RESTRICT"
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
    "ESCAPED_NEWLINE",
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
        """Updates informations about the context and  the scope if needed
            after a primary rule has succeeded.
            Do nothing on empty lines since they can be anywhere
        """
        if len(self.history) > 0 and self.history[-1] == "IsEmptyLine":
            return
        if self.sub is not None:
            self.scope = self.sub
            self.sub = None
        if type(self.scope) is ControlStructure and self.scope.multiline is False and self.scope.lines > 0:
            self.scope = self.scope.outer()
            self.sub = None
            self.update()
        self.arg_pos = [0, 0]

    def dprint(self, rule, pos):
        """Debug printing, shows the primary rules that succeed in matching
            tokens and print the matching tokens
        """
        if self.debug is False:
            return
        print(f"{colors(self.filename, 'cyan')} - {colors(rule, 'green')} \
In \"{self.scope.name}\" from \
\"{self.scope.parent.name if self.scope.parent is not  None else None}\" line {self.tokens[0].pos[0]}\":")
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
        if pos - 1 < len(self.tokens) and self.tokens[pos - 1].type != "NEWLINE":
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

    def skip_ws(self, pos, nl=False):
        ws = whitespaces[:]
        if nl == False:
            ws.remove("NEWLINE")
        while self.check_token(pos, ws):
            pos += 1
        return pos


    def skip_nest_reverse(self, pos):
        """Skips anything between two brackets, parentheses or braces starting
            at 'pos', if the brackets, parentheses or braces are not closed or
            are closed in the wrong order an error shall be raised
        """
        rbrackets = ["LBRACKET", "LBRACE", "LPARENTHESIS"]
        lbrackets = ["RBRACKET", "RBRACE", "RPARENTHESIS"]
        c = self.peek_token(pos).type
        if c not in lbrackets:
            return pos
        c = rbrackets[lbrackets.index(c)]
        i = pos - 1
        while self.peek_token(i) is not None:
            if self.check_token(i, lbrackets) is True:
                i = self.skip_nest(i)
                if i == -1:
                    return -1
            elif self.check_token(i, rbrackets) is True:
                if c == self.peek_token(i).type:
                    return i
            i -= 1
        raise CParsingError("Nested parentheses, braces or brackets\
 are not correctly closed")

        return -1

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
            i += 1
        raise CParsingError("Nested parentheses, braces or brackets\
 are not correctly closed")

        return -1

    def skip_misc_specifier(self, pos, nl=False):
        i = self.skip_ws(pos, nl=nl)
        while self.check_token(i, misc_specifiers):
            i += 1
            i = self.skip_ws(i, nl=nl)
        return i

    def skip_typedef(self, pos):
        i = self.skip_ws(pos)
        if self.check_token(i, "TYPEDEF"):
            i += 1
            i += self.skip_misc_specifier(pos)
        return i

    def check_type_specifier(self, pos, user_def_type=False, nl=False):
        """Returns (True, pos + n) if the tokens from 'pos' to 'n' could match
            a valid type specifier. Valid type specifiers consist of:
                -an optionnal 'misc' specifier (const, register, volatile ...)
                -an optionnal size specifier (long or short)
                -a type specifier (int, char, double, etc...)
                    OR an IDENTIFIER
                    OR a user type specifier (struct, union, enum) + IDENTIFIER
        """
        i = self.skip_misc_specifier(pos, nl=nl)
        i = self.skip_ws(i, nl=nl)
        if user_def_type is True:
            if self.check_token(i, utypes + ["TYPEDEF"]) is True:
                while self.check_token(i, whitespaces + utypes + ["TYPEDEF"]) is True:
                    i += 1
                if self.check_token(i, "IDENTIFIER") is True:
                    i += 1
                    return True, i
                #Raise CParsingError?
            if self.check_token(i, types + ["IDENTIFIER", "TYPEDEF"]) is False:
                return False, 0
            if self.check_token(i, "IDENTIFIER") is True:
                i += 1
                return True, i
            while self.check_token(i, types + whitespaces + ["TYPEDEF"]) is True:
                i += 1
            return True, i
        else:
            if self.check_token(i, utypes) is True:
                i += 1
                i = self.skip_ws(i)
                if self.check_token(i, "IDENTIFIER") is True:
                    i += 1
                    return True, i
            if self.check_token(i, types + ["IDENTIFIER"]) is False:
                return False, 0
            if self.check_token(i, "IDENTIFIER") is True:
                i += 1
                return True, i
            while self.check_token(i, types + whitespaces) is True:
                i += 1
            return True, i

    def check_identifier(self, pos, nl=False):
        i = pos
        p = 0
        i = self.skip_misc_specifier(i, nl=nl)
        while self.check_token(i, whitespaces + ["MULT", "LPARENTHESIS"]) is True:
            i += 1
            if self.check_token(i, "LPARENTHESIS"):
                p += 1

        i = self.skip_misc_specifier(i, nl=nl)
        if self.check_token(i, "IDENTIFIER"):
            while p and self.check_token(i, whitespaces + ["RPARENTHESIS"]) is True:
                if self.check_token(i, "RPARENTHESIS"):
                    p -= 1
                i += 1
            return True, i
        return False, pos

    def is_glued_operator(self, pos):
        """
        Returns True if operator (among +-) at given pos is glued to identifier, number 
        or constant
        """
        not_glued = [
            'IDENTIFIER'
        ]
        glued = [
            'LPARENTHESIS',
            'LBRACKET',
            'LBRACE',
        ]
        glued = glued + glued_operators
        start = pos
        if self.check_token(pos, ['PLUS', 'MINUS']) is False:
            return False
        pos += 1
        pos = self.skip_ws(pos, nl=False)
        if self.check_token(pos, ['IDENTIFIER', 'CONSTANT']) is False:
            return False
        pos = start - 1
        while (self.check_token(pos, ["SPACE", "TAB"])) is True:
            pos -= 1
        if self.check_token(pos, glued) is True:
            return True
        return False

    def is_operator(self, pos):
        """
        Returns True if the given operator (among '*&') is an actual operator,
        and returns False if said operator is a pointer/adress indicator
        """
        i = 0
        start = pos + 1
        pos -= 1
        if self.history[-1] == "IsFuncPrototype" or self.history[-1] == "IsFuncDeclaration":
            return False
        start = self.skip_ws(start, nl=False)
        if self.check_token(start, "RPARENTHESIS") is True:
            return False
        skip = 0
        while pos > 0:
            if self.check_token(pos, ["RBRACKET", "RPARENTHESIS"]) is True:
                pos = self.skip_nest_reverse(pos) - 1
            if self.check_token(pos, ["IDENTIFIER", "CONSTANT", "SIZEOF"]) is True:
                return True
            elif self.check_token(pos, ["LBRACKET", "LPARENTHESIS", "MULT", "BWISE_AND"] + operators):
                return False
            pos -= 1

    def parenthesis_contain(self, i):
        start = i
        ws = ["SPACE", "TAB", "NEWLINE"]
        if self.check_token(i, "RPARENTHESIS") is True:
            while i > 0 and self.check_token(i, "LPARENTHESIS") is False:
                i -= 1
        if self.check_token(i, "LPARENTHESIS") is False:
            return None, start
        while self.check_token(i, "RPARENTHESIS") is False:
            if self.check_token(i, ws) is True:
                pass
            if self.check_token(i, ["MULT"]):
                tmp = i + 1
                while self.check_token(tmp, ws) is True:
                    tmp += 1
                if self.check_token(tmp, "IDENTIFIER") is True:
                    return "function", tmp + 1
                return None, start
            if self.check_token(i, "IDENTIFIER") is True:
                tmp = i + 1
                while self.check_token(tmp, ws) is True:
                    tmp += 1
                if self.check_token(tmp, "MULT") is True:
                    return "cast", tmp + 1
                if self.check_token(tmp, "RPARENTHESIS") is True:
                    return "cast", tmp
            if self.check_token(i, types) is True:
                return "cast", i
            i += 1
        return None, start