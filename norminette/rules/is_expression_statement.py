from rules import PrimaryRule
from context import Function, ControlStructure


class IsExpressionStatement(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 0
        self.scope = [Function, ControlStructure]

    def check_instruction(self, context, pos):
        i = context.skip_ws(pos)
        if context.check_token(i, "IDENTIFIER") is False:
            return False,0
        i += 1

        # TO DO:
        # Skip possible brackets:
        # eg: "f[0]();" is a valid instruction

        i = context.skip_ws(i)
        if context.check_token(i, "LPARENTHESIS") is False:
            return False, 0

        # Shouldn't use skip_nest, should parse manually
        i = context.skip_nest(i)
        print(context.peek_token(i))
        return True, i


    def check_cast(self, context, pos):
        pass

    def run(self, context):
        i = 0
        ret, i = self.check_instruction(context, 0)
        if ret is False:
            return False, 0
        i += 1
        i = context.eol(i)
        return True, i
    pass
