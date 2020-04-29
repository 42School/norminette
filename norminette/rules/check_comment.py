from rules import Rule
from scope import *

class CheckComment(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsComment"]

    def run(self, context):
        i = context.skip_ws(0)
        if context.scope.name != "GlobalScope":
            context.new_error("WRONG_SCOPE_COMMENT", context.peek_token(i))
            return True, i
        return False, 0
