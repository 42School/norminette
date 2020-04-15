from rules import PrimaryRule
from context import Function, ControlStructure


keywords = [
    "BREAK",
    "CONTINUE",
    "GOTO",
    "RETURN"
]

operators = [
    "MULT",
    "LPARENTHESIS",
    "RPARENTHESIS",
    "LBRACKET",
    "RBRACKET",
    "PTR",
    "DOT"
]

ws = ["SPACE", "TAB","NEWLINE"]

class IsExpressionStatement(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 0
        self.scope = [Function, ControlStructure]

    def check_reserved_keywords(self, context, pos):
        if context.check_token(pos, keywords) is False:
            return False, pos
        if context.check_token(pos, "RETURN"):
            i = pos + 1
            while context.check_token(i, "SEMI_COLON") is False:
                i += 1
            i += 1
            return True, i
        elif context.check_token(pos, "GOTO"):
            i = pos + 1
            i = context.skip_ws(i)
            if context.check_token(i, "IDENTIFIER") is False:
                raise CParsingError("Goto statement should be followed by \
a label")
            i += 1
            i = context.skip_ws(i)
            i += 1
            return True, i
        else:
            i = pos + 1
            i = context.skip_ws(i)
            i += 1
            return True, i

    def check_instruction(self, context, pos):
        i = pos
        if context.check_token(i, ["IDENTIFIER"]) is False:
            return False, pos
        i += 1
        # TO DO:
        # Skip possible brackets:
        # eg: "f[0]();" is a valid instruction

        i = context.skip_ws(i)
        if context.check_token(i, "LPARENTHESIS") is False:
            return False, pos

        # Shouldn't use skip_nest, should parse manually ?
        i = context.skip_nest(i)
        i += 1
        i = context.skip_ws(i)
        if context.check_token(i, "SEMI_COLON") is False:
            return False, pos
        i += 1
        # print(context.peek_token(i))
        return True, i

    def check_inc_dec(self, context, pos):
        i = pos
        ret = False
        if context.check_token(i, ["INC", "DEC"]) is True:
            ret = True
            i += 1
            i = context.skip_ws(i)
        if context.check_token(i, "LPARENTHESIS") is True:
            i = context.skip_nest(i)
            i += 1
            i = context.skip_ws(i)
            if ret is False:
                if context.check_token(i, ["INC", "DEC"]) is False:
                    return False, pos
                i += 1
                i = context.skip_ws(i)
            if context.check_token(i, "SEMI_COLON") is False:
                return False, pos
            i += 1
            return True, i
        if context.check_token(i, "IDENTIFIER") is True:
            i += 1
            if ret is False:
                i = context.skip_ws(i)
                if context.check_token(i, ["INC", "DEC"]) is False:
                    return False, pos
                i += 1
                i = context.skip_ws(i)
            while context.check_token(i, "SEMI_COLON") is False:
                i += 1
            i += 1
            return True, i
        return False, pos

    """
    def skip_cast(self, context, pos):
        p = 0
        while context.check_token(i. ws + ["LPARENTHESIS", "MULT"]) is True:
            if context.check_token(i, "LPARENTHESIS") is True:
                p += 1
            i += 1

        if context.check_token(i, "IDENTIFIER") is False:
            return False, pos

        i += 1
        while context.check_token(i, ws + ["MULT"]) is True:
            i += 1
        while context.check_token(i, ws + ["RPARENTHESIS"]) is True:
            if context.check_token(i, "RPARENTHESIS") is True:
                p -= 1
            i += 1

        if p:
            return False, 0

        return True, i
    """
    def run(self, context):
        i = context.skip_ws(0)
        ret, i = self.check_instruction(context, i)
        if ret is False:
            ret, i = self.check_reserved_keywords(context, i)
            if ret is False:
                ret, i = self.check_inc_dec(context, i)
                if ret is False:
                    return False, 0
        i = context.eol(i)
        return True, i
    pass
