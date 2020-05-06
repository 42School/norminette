from rules import Rule
from scope import *

forbidden_cs = [
    "FOR",
    "SWITCH",
    "CASE",
    "GOTO"
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

class CheckControlStatement(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsControlStatement"]

    def check_nest(self, context, i):
        while context.check_token(i, "RPARENTHESIS") is False:
            if context.check_token(i, assigns) is True:
                context.new_error("ASSIGN_IN_CONTROL", context.peek_token(i))
            if context.check_token(i, forbidden_cs) is True:
                context.new_error("FORBIDDEN_CS", context.peek_token(i))
            i += 1
        return

    def run(self, context):
        i = 0
        while context.check_token(i, "NEWLINE") is False:
            if context.check_token(i, forbidden_cs) is True:
                context.new_error("FORBIDDEN_CS", context.peek_token(i))
                return True, i
            elif context.check_token(i, "LPARENTHESIS") is True:
                self.check_nest(context, i)
            i += 1
        return False, 0
