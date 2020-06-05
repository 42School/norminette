from rules import PrimaryRule
from context import GlobalScope, VariableAssignation
from exceptions import CParsingError


assign_ops = [
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
    "ASSIGN"
]

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
    "STRUCT",
    "ENUM",
    "UNION",
    "CONST",
    "REGISTER",
    "STATIC",
    "VOLATILE"
]

op = [
    "MULT",
    "LPARENTHESIS",
    "RPARENTHESIS",
    "LBRACKET",
    "RBRACKET",
    "MINUS",
    "PLUS",
    "DIV",
    "INC",
    "DEC",
    "PTR",
    "DOT"
]

ws = ["SPACE", "TAB", "NEWLINE"]


class IsFunctionCall(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.primary = True
        self.priority = 11
        self.scope = []

    def run(self, context):
        i = context.skip_ws(0, nl=False)
        types = []
        while context.check_token(i, "LPARENTHESIS") is True:
            typ, i = context.parenthesis_contain(i)
            types.append(typ)
            if typ == None:
                i = context.skip_ws(i + 1)
                if context.check_token(i, "IDENTIFIER") is True:
                    i += 1
                    i = context.skip_ws(i)
                    if context.check_token(i, "LPARENTHESIS") is True:
                        i = context.skip_nest(i)
                        while context.peek_token(i) is not None and context.check_token(i, ["SEMI_COLON", "NEWLINE"]) is False:
                            i += 1
                        if context.peek_token(i) is None or context.check_token(i, "NEWLINE") is True:
                            return False
                        i += 1
                        i = context.eol(i)
                        return True, i
            elif typ == "function" or typ == "cast":
                i += 1
                i = context.skip_ws(i)
        if context.check_token(i, "IDENTIFIER") is True:
            i += 1
            i = context.skip_ws(i)
            if context.check_token(i, "LPARENTHESIS") is True:
                i = context.skip_nest(i)
                while context.peek_token(i) is not None and context.check_token(i, "SEMI_COLON") is False:
                    i += 1
                i += 1
                i = context.eol(i)
                return True, i
        return False, 0