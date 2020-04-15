from rules import PrimaryRule
from context import ControlStructure, Function


cs_keywords = ["DO", "WHILE", "FOR", "IF", "ELSE", "SWITCH"]
whitespaces = ["TAB", "SPACE", "NEWLINE"]


class IsEmptyLine(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 0
        self.scope = []

    def run(self, context):
        i = 0
        while context.check_token(i, ["SPACE", "TAB"]) is True:
            i += 1
        i += 1
        if context.check_token(i, "NEWLINE") is True:
            return True, i
        return False, 0
