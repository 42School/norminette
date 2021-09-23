from norminette.rules import PrimaryRule
import pdb

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
    "INC",
    "DEC",
]

SEPARATORS = [
    "COMMA",
    "AND",
    "OR",
    "SEMI_COLON"
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
    "PTR",
    "DOT",
]

ws = ["SPACE", "TAB", "NEWLINE"]


class IsAssignation(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.primary = True
        self.priority = 20
        self.scope = []

    def skip_ptr(self, context, pos):
        i = context.skip_ws(pos)
        while context.check_token(i, operators + ws + ["IDENTIFIER"]) is True:
            i += 1
        return i

    def check_identifier(self, context, pos):
        i = pos
        while context.check_token(i, types + ws + op + ["IDENTIFIER", "CONSTANT", "INC", "DEC"]):
            if context.check_token(i, "LBRACKET"):
                i = context.skip_nest(i)
            i += 1
        if "IDENTIFIER" in [t.type for t in context.tokens[: i + 1]]:
            return True, i
        else:
            return False, 0

    def parse_assign_right_side(self, context, i):
        while context.check_token(i, SEPARATORS) is False:
            if context.check_token(i, ["LBRACE", "LPARENTHESIS", "LBRACKET"]):
                i = context.skip_nest(i)
            i += 1
        return i


    def run(self, context):
        """
        Catches all assignation instructions
        Requires assign token
        """
        ret, i = self.check_identifier(context, 0)
        if ret is False:
            return False, 0
        tmp = 0
        while context.check_token(tmp, assign_ops) is False and tmp <= i:
            tmp += 1
        if context.check_token(tmp, assign_ops) is False:
            return False, 0
        i = tmp + 1
        #i += 1
        i = context.skip_ws(i)
        # if context.check_token(i, "LBRACE") is True:
        # i += 1
        # context.sub = context.scope.inner(VariableAssignation)
        # return True, i
        if context.scope.name == "UserDefinedEnum":
            while context.peek_token(i) and (context.check_token(i, ["COMMA", "SEMI_COLON", "NEWLINE"])) is False:
                i += 1
            i = context.eol(i)
            return True, i
        i = self.parse_assign_right_side(context, i)
        # while context.check_token(i, SEPARATORS) is False:
        #     i += 1
        #     if context.peek_token(i) is None:
        #         return False, 0
        i += 1
        i = context.eol(i)
        return True, i
