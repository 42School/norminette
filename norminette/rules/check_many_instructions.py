from lexer import Token
from rules import Rule
import string


class CheckManyInstructions(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = [
                        "IsAssignation",
                        "IsBlockEnd",
                        "IsComment",
                        "IsControlStatement",
                        "IsExpressionStatement",
                        "IsFuncDeclaration",
                        "IsFuncPrototype",
                        "IsUserDefinedType",
                        "IsVarDeclaration"]

    def run(self, context):
        """
        Raises 1018 error, bad formated user defined identifier
        """
        if context.peek_token(0).pos[1] > 1:
            context.new_error(1024, context.peek_token(0))
        return False, 0
