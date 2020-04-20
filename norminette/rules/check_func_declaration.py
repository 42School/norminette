from rules import Rule
from scope import *

class CheckFuncDeclaration(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsFuncDeclaration"]

    def run(self, context):
        i = 0
        if len(context.history) > 1 and context.history[-2] != "IsEmptyLine":
            context.new_error("NEWLINE_PRECEDES_FUNC", context.peek_token(i))
            return True, i
        return False, 0
