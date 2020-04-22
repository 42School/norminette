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

    def run(self, context):
        i = 0
        assign_present = False
        while context.check_token(i, "SEMI_COLON") is False:
            if context.check_token(i, assigns) is True and assign_present == False:
                assign_present = True
            elif context.check_token(i, assigns) is True and assign_present == True:
                context.new_error("MULT_ASSIGN_LINE", context.peek_token(i))
            i += 1
        return False, 0
