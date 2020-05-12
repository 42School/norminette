from lexer import Token
from rules import PrimaryRule
from context import (
                    Function,
                    UserDefinedType,
                    VariableAssignation,
                    ControlStructure)


class IsBlockStart(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 10
        self.scope = [
                        Function,
                        UserDefinedType,
                        VariableAssignation,
                        ControlStructure]

    def run(self, context):
        i = context.skip_ws(0, nl=False)
        if context.check_token(i, "LBRACE") is False:
            return False, 0
        i += 1
        context.scope.multiline = True
        while (context.check_token(i, "NEWLINE")) is False:
            i += 1
        i = context.eol(i)
        return True, i
