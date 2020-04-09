from rules import PrimaryRule
from context import Function, ControlStructure


keywords = [
    "BREAK",
    "CONTINUE",
    "GOTO",
    "RETURN"
]


class IsExpressionStatement(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 0
        self.scope = [Function, ControlStructure]

    def check_instruction(self, context, pos):
        i = context.skip_ws(pos)
        if context.check_token(i, ["IDENTIFIER"] + keywords) is False:
            return False, 0
        i += 1
        # TO DO:
        # Skip possible brackets:
        # eg: "f[0]();" is a valid instruction

        i = context.skip_ws(i)
        if context.check_token(i, "LPARENTHESIS") is False:
            return False, 0

        # Shouldn't use skip_nest, should parse manually ?
        i = context.skip_nest(i)
        i += 1
        i = context.skip_ws(i)
        if context.check_token(i, "SEMI_COLON") is False:
            return False, 0
        i += 1
        # print(context.peek_token(i))
        return True, i


    def skip_cast(self, context, pos):
        ws = ["SPACE", "TAB","NEWLINE"]
        p = 0
        while context.check_token(i. ws + ["LPARENTHESIS"]) is True:
            if context.check_token(i, "LPARENTHESIS") is True:
                p += 1
            i += 1

        if context.check_token(i, "IDENTIFIER") is False:
            return False, pos

        i += 1
        while context.check_token(i. ws + ["MULT"]) is True:
            i += 1
        while context.check_token(i, ws + ["RPARENTHESIS"]) is True:
            if context.check_token(i, "RPARENTHESIS") is True:
                p -= 1
            i += 1

        if p:
            return False, pos

        return True, i

    def run(self, context):
        i = 0
        ret, i = self.check_instruction(context, 0)
        if ret is False:
            return False, 0
        i = context.eol(i)
        return True, i
    pass
