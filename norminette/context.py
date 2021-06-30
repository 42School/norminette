from norminette.exceptions import CParsingError
from norminette.lexer.dictionary import operators
from norminette.norm_error import NormError
from norminette.scope import GlobalScope, ControlStructure
from norminette.tools.colors import colors
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
    "UNSIGNED",
]

utypes = ["STRUCT", "ENUM", "UNION"]

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
    "AND_ASSIGN",
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
    "AND_ASSIGN",
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
    "CASE",
]
misc_specifiers = [
    "CONST",
    "RESTRICT",
    "REGISTER",
    "STATIC",
    "VOLATILE",
    "EXTERN",
    "INLINE",
    "RESTRICT" "SIGNED",
    "UNSIGNED",
]

assigns = [
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
    "ASSIGN",
]

size_specifiers = ["LONG", "SHORT"]

sign_specifiers = ["SIGNED", "UNSIGNED"]

whitespaces = ["SPACE", "TAB", "ESCAPED_NEWLINE", "NEWLINE"]

arg_separator = ["COMMA", "CLOSING_PARENTHESIS"]


class Context:
    def __init__(self, filename, tokens, debug=0, added_value=[]):
        # File relative informations
        self.filename = filename
        self.filetype = filename.split(".")[-1]  # ?
        self.tokens = tokens
        self.debug = int(debug)

        # Rule relative informations
        self.history = []
        self.errors = []
        self.tkn_scope = len(tokens)

        # Scope informations
        self.scope = GlobalScope()
        self.func_alignment = 0
        self.sub = None
        self.fname_pos = 0
        self.arg_pos = [0, 0]

        # Preprocessor handling
        self.preproc_scope_indent = 0
        self.skip_define_error = True if added_value is not None and "CheckDefine" in added_value else False

    def peek_token(self, pos):
        return self.tokens[pos] if pos < len(self.tokens) else None

    def pop_tokens(self, stop):
        self.tokens = self.tokens[stop:]

    def check_token(self, pos, value):
        """Compares the token at 'pos' against a value or list of values"""
        tkn = self.peek_token(pos)

        if tkn is None:
            return None

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
        if len(self.history) > 0 and (
            self.history[-1] == "IsEmptyLine"
            or self.history[-1] == "IsComment"
            or self.history[-1] == "IsPreprocessorStatement"
        ):
            return
        if self.sub is not None:
            self.scope = self.sub
            self.sub = None
        if type(self.scope) is ControlStructure and self.scope.multiline is False and self.scope.instructions > 0:
            self.scope = self.scope.outer()
            self.sub = None
            self.update()
        self.arg_pos = [0, 0]

    def dprint(self, rule, pos):
        """Debug printing, shows the primary rules that succeed in matching
        tokens and print the matching tokens
        """
        if self.debug < 2:
            return
        print(
            f"{colors(self.filename, 'cyan')} - {colors(rule, 'green')} \
In \"{self.scope.name}\" from \
\"{self.scope.parent.name if self.scope.parent is not  None else None}\" line {self.tokens[0].pos[0]}\":"
        )
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
        try:
            c = self.peek_token(pos).type
        except:
            raise CParsingError(f"Error: Unexpected EOF line {pos}")
        if c not in lbrackets:
            return pos
        c = rbrackets[lbrackets.index(c)]
        i = pos - 1
        while self.peek_token(i) is not None:
            if self.check_token(i, lbrackets) is True:
                i = self.skip_nest_reverse(i)
                if i == -1:
                    return -1
            elif self.check_token(i, rbrackets) is True:
                if c == self.peek_token(i).type:
                    return i
            i -= 1
        raise CParsingError(
            "Error: Nested parentheses, braces or brackets\
 are not correctly closed"
        )

        return -1

    def skip_nest(self, pos):
        """Skips anything between two brackets, parentheses or braces starting
        at 'pos', if the brackets, parentheses or braces are not closed or
        are closed in the wrong order an error shall be raised
        """
        lbrackets = ["LBRACKET", "LBRACE", "LPARENTHESIS"]
        rbrackets = ["RBRACKET", "RBRACE", "RPARENTHESIS"]
        try:
            c = self.peek_token(pos).type
        except:
            raise CParsingError(f"Error: Code ended unexpectedly.")
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
        raise CParsingError(
            "Error: Nested parentheses, braces or brackets\
 are not correctly closed"
        )

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
                # Raise CParsingError?
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
                return True, i + 1
            while self.check_token(i, types + whitespaces + ["MULT", "BWISE_AND"]) is True:
                i += 1
            i = self.skip_misc_specifier(i, nl=nl)
            return True, i

    def check_identifier(self, pos, nl=False):
        """
        Determines the function return value or the variable type and returns
        an iterator to the next token
        """
        i = pos
        p = 0
        i = self.skip_misc_specifier(i, nl=nl)
        while self.check_token(i, whitespaces + ["MULT", "LPARENTHESIS"]) is True:
            if self.check_token(i, "LPARENTHESIS"):
                p += 1
            if self.check_token(i, "MULT") and self.check_token(i + 1, "CONST"):
                i += 1
            i += 1
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
        glued = [
            "LPARENTHESIS",
            "LBRACKET",
            "LBRACE",
        ]
        glued = glued + glued_operators
        start = pos
        if (
            self.check_token(
                pos,
                ["PLUS", "MINUS", "BWISE_OR", "BWISE_AND", "BWISE_NOT", "BWISE_XOR"],
            )
            is False
        ):
            return False
        pos += 1
        pos = self.skip_ws(pos, nl=False)
        if self.check_token(pos, ["IDENTIFIER", "CONSTANT"]) is False:
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
        if self.check_token(start, ["RPARENTHESIS", "MULT"]) is True:
            return False
        start = self.skip_ws(start, nl=False)
        if self.check_token(start, ["SIZEOF"]) is True:
            return True
        if self.history[-1] == "IsVarDeclaration":
            bracketed = False
            tmp = pos
            right_side = False
            while tmp > 0:
                if self.check_token(tmp, ["RBRACKET", "RPARENTHESIS"]) is True:
                    tmp = self.skip_nest_reverse(tmp) - 1
                if self.check_token(tmp, ["ASSIGN"]) is True:
                    right_side = True
                if self.check_token(tmp, "LBRACKET") is True:
                    bracketed = True
                tmp -= 1
            if right_side == False and bracketed == False:
                return False
        skip = 0
        value_before = False
        while pos > 0:
            if self.check_token(pos, ["RBRACKET", "RPARENTHESIS"]) is True:
                value_before = True
                pos = self.skip_nest_reverse(pos) - 1
                if self.check_token(pos + 1, "LPARENTHESIS") is True and self.parenthesis_contain(pos + 1)[0] == "cast":
                    return False
                skip = 1
            if self.check_token(pos, ["IDENTIFIER", "CONSTANT", "SIZEOF", "CHAR_CONST"]) is True:
                if self.check_token(pos, "IDENTIFIER") is True and self.check_token(pos + 1, "TAB") is True:
                    return False
                return True
            if self.check_token(pos, ["COMMA", "LPARENTHESIS"] + operators) is True and skip == 1 and self.parenthesis_contain(pos + 1)[0] != "cast":
                return True
            if self.check_token(pos, ["LBRACKET", "LPARENTHESIS", "MULT", "BWISE_AND", "COMMA"] + operators + types):
                return False
            pos -= 1
        if value_before == True:
            return True
        else:
            return False

    def parenthesis_contain(self, i, ret_store=None):
        """
        Explore parenthesis to return its content
        Function, pointer, cast, or other
        Uses basic string as return value and skips to the end of the parenthesis nest
        """
        if self.check_token(i, "LPARENTHESIS") is False:
            return None, i
        start = i
        ws = ["SPACE", "TAB", "NEWLINE"]
        i += 1
        deep = 1
        nested_id = False
        identifier = None
        pointer = None
        sizeof = False
        if self.check_token(start - 1, "SIZEOF") is True:
            sizeof = True
        i = self.skip_ws(i)
        while deep > 0:
            #print (self.peek_token(i), deep, identifier, self.check_token(i, "NULL"))
            if self.check_token(i, "RPARENTHESIS"):
                deep -= 1
            elif self.check_token(i, "LPARENTHESIS"):
                deep += 1
                #if identifier is not None and deep >= 0:
                    #return "pointer", self.skip_nest(start)
            elif deep > 1 and identifier == True and self.check_token(i, ["NULL", "IDENTIFIER"]):
                return "fct_call", self.skip_nest(start)
            elif self.check_token(i, "COMMA") and nested_id == True:
                return "function", self.skip_nest(start)
            elif self.check_token(i, "COMMA"):
                return None, self.skip_nest(start)
            elif self.check_token(i, ws):
                pass
            elif self.check_token(i, types):
                tmp = start - 1
                while self.check_token(tmp, ["SPACE", "TAB"]) == True:
                    tmp -= 1
                if self.check_token(tmp, "SIZEOF") == True:
                    return None, self.skip_nest(start)
                tmp = start + 1
                while self.check_token(tmp, "RPARENTHESIS") is False:
                    if self.check_token(tmp, ["LPARENTHESIS", "IDENTIFIER"]) is True:
                        return None, self.skip_nest(start)
                    tmp += 1
                if deep == 1:
                    return "cast", self.skip_nest(start)
            elif self.check_token(i, "IDENTIFIER"):
                tmp = i + 1
                if (identifier is not True and pointer == True) or ret_store is not None:
                    nested_id = True
                if identifier is not True and self.check_token(tmp, "RPARENTHESIS") and self.scope.name == "Function" and deep == 1 and pointer == None and sizeof == False:
                    tmp = self.skip_nest(start) + 1
                    tmp = self.skip_ws(tmp)
                    if self.check_token(tmp, "IDENTIFIER") is False:
                        return None, self.skip_nest(start)
                    return "cast", self.skip_nest(start)
                identifier = True
                tmp = self.skip_ws(tmp)
                if pointer == True:
                    if self.check_token(tmp, "LBRACKET"):
                        tmp = self.skip_nest(tmp)
                        tmp += 1
                    while self.check_token(tmp, "RPARENTHESIS"):
                        tmp += 1
                        # start = tmp
                    tmp = self.skip_ws(tmp)
                    if self.check_token(tmp, "LPARENTHESIS"):
                        return "pointer", self.skip_nest(start)
                    elif self.check_token(tmp, "RPARENTHESIS"):
                        return None, self.skip_nest(start)
            elif self.check_token(i, ["MULT", "BWISE_AND"]):
                tmp = i + 1
                pointer = True
                if identifier != None:
                    tmp = start - 1
                    while self.check_token(tmp, ["SPACE", "TAB"]) == True:
                        tmp -= 1
                    if self.check_token(tmp, "SIZEOF") == True:
                        return None, self.skip_nest(start)
                    tmp = self.skip_ws(i + 1)
                    if self.check_token(tmp, "RPARENTHESIS") is True:
                        return "cast", self.skip_nest(start)
            i += 1
        return None, self.skip_nest(start)
