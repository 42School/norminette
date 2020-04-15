from rules import PrimaryRule
from context import (
                        GlobalScope,
                        Function,
                        ControlStructure,
                        UserDefinedType,
                        VariableAssignation)

whitespaces = ["SPACE", "TAB", "NEWLINE"]


class IsEndOfLine(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 1
        self.scope = [
                        GlobalScope,
                        Function,
                        ControlStructure,
                        UserDefinedType,
                        VariableAssignation]

    def run(self, context):
        return False, 0
        i = 0
        while context.check_token(i, whitespaces):
            i += 1
        if context.check_token(i, "NEWLINE"):
            return True, i + 1
        return False, 0
