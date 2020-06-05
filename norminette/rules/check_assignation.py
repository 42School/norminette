from rules import Rule
from scope import *
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


class CheckAssignation(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsAssignation"]

    def check_assign_right(self, context, i):
        typ = None
        tmp_typ = None
        while context.check_token(i, "SEMI_COLON") is False:
            if context.check_token(i, "LPARENTHESIS") is True:
                tmp_typ, i = context.parenthesis_contain(i)
                if tmp_typ != None:
                    typ = tmp_typ
                if tmp_typ is None:
                    tmp = i + 1
                    while context.check_token(tmp, "RPARENTHESIS") is False:
                        if context.check_token(tmp, "COMMA") is True and typ != "function":
                            context.new_error("TOO_MANY_INSTR", context.peek_token(tmp))
                        tmp += 1
            if context.check_token(i, assigns) is True:
                context.new_error("MULT_ASSIGN_LINE", context.peek_token(i))
            i += 1
        return False, 0

    def run(self, context):
        i = 0
        assign_present = False
        while context.check_token(i, "SEMI_COLON") is False:
            if context.check_token(i, assigns) is True and assign_present == False:
                assign_present = True
                return self.check_assign_right(context, i + 1)
            i += 1
        return False, 0
