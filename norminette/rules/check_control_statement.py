from rules import Rule
from scope import *

forbidden_cs = [
    "FOR",
    "SWITCH",
    "CASE",
    "GOTO"
]

class CheckControlStatement(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsControlStatement"]

    def run(self, context):
        i = 0
        while context.check_token(i, "NEWLINE") is False:
            if context.check_token(i, forbidden_cs) is True:
                context.new_error("FORBIDDEN_CS", context.peek_token(i))
                return True, i
            i += 1
        return False, 0
