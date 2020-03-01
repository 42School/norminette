from lexer import Token
from rules import Rule
import string


class CheckFuncName(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["CheckFuncDeclarations"]

    def run(self, context):
        legal_characters = string.ascii_lowercase + string.digits + '_'
        for c in context.scope.fnames[-1]:
            if c not in legal_characters:
                context.new_error(1018, context.peek_token(context.fname_pos))
                break
        return False, 0
