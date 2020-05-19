from lexer import Token
from rules import Rule
import string

class CheckTernary(Rule):
    def __init__(self):
        super().__init__()
        self.priority = 10
        self.depends_on = ['IsTernary']

    def run(self, context):
        context.new_error("TERNARY_FBIDDEN", context.peek_token(0))
        return False, 0
