from lexer import Token
from rules import Rule
import string

class IsTernary(Rule):
    def __init__(self):
        super().__init__()
        self.priority = 10
        self.scope = []

    def run(self, context):
        i = 0
        while context.check_token(i, "SEMI_COLON") is False:
            if context.check_token(i, "TERN_CONDITION") is True:
                while context.check_token(i, "SEMI_COLON") is False:
                    i += 1
                i += 1
                i = context.eol(i)
                return True, i
            i += 1
        return False, 0
