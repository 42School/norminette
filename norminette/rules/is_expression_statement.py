from rules import PrimaryRule
from context import Function, ControlStructure


class IsExpressionStatement(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 0
        self.scope = [Function, ControlStructure]

    def check_instruction(self, context, pos):
        pass

    def check_cast(self, context, pos):
        pass

    def run(self, context):
        i = 0
        #print(context.tokens[0:])
        while context.peek_token(i) is not None:
            if context.check_token(i, "SEMI_COLON") is True:
                break
            i += 1
        else:
            return False, 0
        i += 1
        i = context.eol(i)
        return True, i
    pass
