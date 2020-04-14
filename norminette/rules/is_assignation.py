from rules import PrimaryRule
from context import GlobalScope, VariableAssignation


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


class IsAssignation(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.primary = True
        self.priority = 5
        self.scope = []

    def run(self, context):
        i = context.skip_ws(0)
        if context.check_identifier(i) is False:
            return False, 0
        i += 1
        i = context.skip_ws(i)
        if context.check_token(i, "LBRACKET"):
            i = context.skip_nest(i)
            i += 1
            i = context.skip_ws(i)
        if context.check_token(i, assign_ops) is False:
            return False, 0
        i += 1
        i = context.skip_ws(i)
        if context.check_token(i, "LBRACE") is True:
            i += 1
            context.sub = context.scope.inner(VariableAssignation)
            return True, i
        while context.check_token(i, "SEMI_COLON") is False:
            i += 1
            if context.peek_token(i) is None:
                return False, 0
        i += 1
        i = context.eol(i)
        return True, i
