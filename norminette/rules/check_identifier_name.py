from lexer import Token
from rules import Rule
import string


class CheckIdentifierName(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = []

    def run(self, context):
        """
        Raises 1018 error, bad formated user defined identifier
        """
        legal_characters = string.ascii_lowercase + string.digits + '_' + '&*'
        if context.history[-1] == "IsFuncDeclaration" or context.history[-1] == "IsFuncPrototype":
            for c in context.scope.fnames[-1]:
                if c not in legal_characters:
                    context.new_error(
                                    "FORBIDDEN_CHAR_NAME",
                                    context.peek_token(context.fname_pos))
                    break
        else:
            _, i = context.check_type_specifier(0)
            while context.check_token(i, "IDENTIFIER") is False:
                i += 1
            for c in context.peek_token(i).value:
                if c not in legal_characters:
                    context.new_error(
                                    "FORBIDDEN_CHAR_NAME",
                                    context.peek_token(context.fname_pos))
                    break

        return False, 0
