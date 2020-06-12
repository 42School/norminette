from rules import PrimaryRule
from context import ControlStructure, Function, GlobalScope
from exceptions import CParsingError

cs_keywords = ["DO", "WHILE", "FOR", "IF", "ELSE", "SWITCH", "CASE", "DEFAULT", "IDENTIFIER"]
whitespaces = ["TAB", "SPACE", "NEWLINE"]


class IsControlStatement(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 12
        self.scope = [Function, ControlStructure, GlobalScope]

    def run(self, context):
        is_id = False
        i = context.skip_ws(0, nl=False)
        if context.check_token(i, cs_keywords) is False:
            return False, 0
        if context.check_token(i, "IDENTIFIER") is True:
            is_id = True
        if context.check_token(i, ["SWITCH", "CASE", "DEFAULT"]) is True:
            i += 1
            i = context.skip_ws(i, nl=False)
            if context.check_token(i, "LPARENTHESIS") is True:
                i = context.skip_nest(i)
            i = context.skip_ws(i, nl=False)
            if context.check_token(i, ["CONSTANT", "IDENTIFIER"]) is True:
                i += 1
            i = context.skip_ws(i, nl=False)
            context.sub = context.scope.inner(ControlStructure)
            context.sub.multiline = False
            if context.check_token(i, "COLON") is True:
                i += 1
                i = context.eol(i)
                return True, i
            else:
                while context.check_token(i, ["NEWLINE"]) is False:
                    i += 1
                i = context.eol(i)
                return True, i
        if context.check_token(i, "ELSE") is True:
            i += 1
            while context.check_token(i, ["TAB", "SPACE"]) is True:
                i += 1
            if context.check_token(i, "SEMI_COLON") is True:
                i += 1
                i = context.eol(i)
                return True, i
            if context.check_token(i, "NEWLINE") is True:
                context.sub = context.scope.inner(ControlStructure)
                context.sub.multiline = False
                i = context.eol(i)
                return True, i
            if context.check_token(i, ["IF"]) is True:
                i += 1
                pass
            elif context.check_token(i, ["LBRACE", "COMMENT", "MULT_COMMENT"]) is False:
                raise CParsingError(f"{context.filename}: Error parsing line {context.peek_token(0).pos[0]}")
            else:
                context.sub = context.scope.inner(ControlStructure)
                context.sub.multiline = False
                i = context.eol(i)
                return True, i
        i += 1
        i = context.skip_ws(i, nl=False)
        if context.check_token(i, "LPARENTHESIS") is False:
            return False, 0
        i = context.skip_nest(i)
        i += 1
        i = context.skip_ws(i, nl=False)
        if context.check_token(i, "SEMI_COLON") is True:
            if is_id == True:
                return False, 0
            i += 1
            i = context.eol(i)
            return True, i
        context.sub = context.scope.inner(ControlStructure)
        context.sub.multiline = False
        i = context.eol(i)
        return True, i
