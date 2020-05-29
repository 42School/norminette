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
        tmp = i
        while context.peek_token(tmp) and (context.check_token(tmp, "NEWLINE")) is False:
            tmp += 1
        tmp = context.eol(tmp)
        if context.peek_token(tmp) is not None:
            i = tmp
        return True, i
