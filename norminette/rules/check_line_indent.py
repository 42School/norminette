from rules import Rule
from scope import *



class CheckLineIndent(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = []

    def run(self, context):
        expected = context.scope.indent
        if context.history[-1] == "IsEmptyLine":
            return False, 0
        got = 0
        while context.check_token(got, "TAB"):
            got += 1
        if context.check_token(got, ["LBRACE", "RBRACE"]) and expected > 0:
            expected -= 1
        if expected > got:
            context.new_error("TOO_FEW_TAB", context.peek_token(0))
            return False, 0
        elif got > expected:
            context.new_error("TOO_MANY_TAB", context.peek_token(0))
            return False, 0
        return False, 0