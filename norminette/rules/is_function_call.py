from norminette.rules import PrimaryRule

condition_ops = [
    "LESS_OR_EQUAL",
    "GREATER_OR_EQUAL",
    "EQUALS",
    "NOT_EQUAL",
    "INC",
    "DEC",
    "AND",
    "OR",
    "BWISE_XOR",
    "BWISE_OR",
    "BWISE_NOT",
    "BWISE_AND",
    "RIGHT_SHIFT",
    "LEFT_SHIFT",
    "DOT",
    "NOT",
    "MINUS",
    "PLUS",
    "MULT",
    "DIV",
    "MODULO",
    "LESS_THAN",
    "MORE_THAN",
]

SEPARATORS = [
    "COMMA",
    "AND",
    "OR",
    "SEMI_COLON"
]

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
    "ASSIGN",
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
    "VOLATILE",
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
    "DOT",
]

ws = ["SPACE", "TAB", "NEWLINE"]


class IsFunctionCall(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.primary = True
        self.priority = 80
        self.scope = []

    def run(self, context):
        """
        Catches function calls when it's in an assignation
        """
        i = context.skip_ws(0, nl=False)
        types = []
        while context.check_token(i, "LPARENTHESIS") is True:
            start = i
            typ, i = context.parenthesis_contain(i)
            types.append(typ)
            if typ == None or typ == "pointer":
                i = context.skip_ws(i + 1)
                if context.peek_token(i) is None or context.check_token(i, "NEWLINE") is True:
                    return False, 0
                # i += 1
                if len(types) > 1:
                    i = context.skip_ws(i, nl=False)
                    if context.check_token(i, SEPARATORS) is True:
                        i += 1
                        i = context.eol(i)
                        return True, i
                    else:
                        return False, 0
            elif typ == "function" or typ == "cast" or typ == "pointer":
                i += 1
                i = context.skip_ws(i)
        while context.check_token(i, ["MULT", "BWISE_AND"]):
            i += 1
        if context.check_token(i, "IDENTIFIER") is True:
            i += 1
            i = context.skip_ws(i)
            if context.check_token(i, "LPARENTHESIS") is True:
                i = context.skip_nest(i)
                while context.peek_token(i) is not None and context.check_token(i, SEPARATORS) is False:
                    i += 1
                i += 1
                i = context.eol(i)
                return True, i
        elif len(types) > 1 and typ == "cast" and (types[-2] == "function" or types[-2] == "pointer"):
            i += 1
            i = context.eol(i)
            return True, i
        return False, 0
