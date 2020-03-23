from rules import Rule
from lexer import Lexer, TokenError

types = [
    "STRUCT",
    "ENUM",
    "UNION",
    "NEWLINE"
]

class CheckStructNaming(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsUserDefinedType"]

    def run(self, context):
        i = 0
        i = context.skip_ws(i)
        while context.check_token(i, types) is False:
            i += 1
        if context.check_token(i, "NEWLINE"):
            return False, 0
        if context.check_token(i, "STRUCT"):
            i += 1
            i = context.skip_ws(i)
            if context.peek_token(i).value.startswith("s_") is False:
                context.new_error("STRUCT_TYPE_NAMING", context.peek_token(i))
        if context.check_token(i, "ENUM"):
            i += 1
            i = context.skip_ws(i)
            if context.peek_token(i).value.startswith("e_") is False:
                context.new_error("ENUM_TYPE_NAMING", context.peek_token(i))
        if context.check_token(i, "UNION"):
            i += 1
            i = context.skip_ws(i)
            if context.peek_token(i).value.startswith("u_") is False:
                context.new_error("UNION_TYPE_NAMING", context.peek_token(i))
        return False, i
