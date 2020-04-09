from rules import PrimaryRule
from context import ControlStructure, Function


cs_keywords = ["DO", "WHILE", "FOR", "IF", "ELSE", "SWITCH"]
whitespaces = ["TAB", "SPACE", "NEWLINE"]


class IsControlStatement(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 10
        self.scope = [Function, ControlStructure]

    def run(self, context):
        i = context.skip_ws(0)
        if context.check_token(i, cs_keywords) is False:
            return False, 0

        i += 1
        i = context.skip_ws(i)
        if context.check_token(i, "LPARENTHESIS") is False:
            # Seems like fatal error
            return False, 0
        i = context.skip_nest(i)
        i += 1
        i = context.skip_ws(i)
        if context.check_token(i, "LBRACE") is False:
            i -= 1
            while context.check_token(i, ["TAB", "SPACE"]) is True:
                i -= 1
            i += 1
            context.sub = context.scope.inner(ControlStructure)
            context.sub.multiline = False
            context.eol(i)
            return True, i
        i += 1
        context.sub = context.scope.inner(ControlStructure)
        context.eol(i)
        return True, i
