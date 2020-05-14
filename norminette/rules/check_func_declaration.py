from rules import Rule
from scope import *

types = [
    "INT",
    "FLOAT",
    "CHAR",
    "DOUBLE",
    "LONG",
    "SHORT"
]

class CheckFuncDeclaration(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsFuncDeclaration", "IsFuncPrototype"]

    def run(self, context):
        i = 0
        tmp = 0
        arg = 1
        while context.check_token(tmp, ["SEMI_COLON", "NEWLINE"]) is False:
            tmp += 1

        #this is a func declaration
        if context.check_token(tmp, "SEMI_COLON") is False:
            if len(context.history) > 1 and context.history[-2] != "IsEmptyLine":
                context.new_error("NEWLINE_PRECEDES_FUNC", context.peek_token(i))
        #this is a func prototype

        i = context.fname_pos + 2
        while context.check_token(i, "RPARENTHESIS") is False:
            if context.check_token(i, "COMMA"):
                arg += 1
            i += 1
        if arg > 4:
            context.new_error("TOO_MANY_ARGS", context.peek_token(i))
        arg = []
        return False, 0
