from rules import PrimaryRule
from context import ControlStructure, Function, GlobalScope
from exceptions import CParsingError

cs_keywords = ["DO", "WHILE", "FOR", "IF", "ELSE", "SWITCH", "CASE", "DEFAULT"]
whitespaces = ["TAB", "SPACE", "NEWLINE"]


class IsAmbiguousDeclaration(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 1
        self.scope = []

    def run(self, context):
        i = context.skip_ws(0, nl=False)
        if context.check_token(i, "SEMI_COLON"):
            i += 1
            i = context.eol(i)
            return True, i
        return False, 0