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
        while context.check_token(i, whitespaces):
            if context.check_token(i, "NEWLINE") is True:
                break
            i += 1
        if context.check_token(i, "LBRACE") is False:
            context.sub = context.scope.inner(ControlStructure)
            context.sub.multiline = False
            return True, i
        context.sub = context.scope.inner(ControlStructure)
        i += 1
        context.eol(i)
        return True, i
