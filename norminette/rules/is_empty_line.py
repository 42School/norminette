from rules import PrimaryRule
from context import (
                        GlobalScope,
                        Function,
                        ControlStructure,
                        UserDefinedType,
                        VariableAssignation)

whitespaces = ["SPACE", "TAB", "NEWLINE"]


class IsEmptyLine(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 0
        self.scope = [
                        GlobalScope,
                        Function,
                        ControlStructure,
                        UserDefinedType,
                        VariableAssignation]

    def run(self, context):
        i = 0
        while context.check_token(i, whitespaces):
            if context.check_token(i, "NEWLINE"):
                break
            i += 1
        else:
            return False, 0
        i += 1
        return True, i
