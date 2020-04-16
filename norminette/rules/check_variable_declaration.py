from rules import Rule
from scope import *



class CheckVariableDeclaration(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsVariableDeclaration"]

    def run(self, context):
        i = 0
        if context.scope.type == "Function":
            if context.history[-2] != "IsBlockStart" and context.history[-2] != "IsVariableDeclaration":
                context.new_error("VAR_DECL_START_FUNC", context.peek_token(i))
            if context.
        elif context.scope.type == "GlobalScope":
            pass
        else:
            context.new_error("WRONG_SCOPE_VAR", context.peek_token(i))
        return False, 0
