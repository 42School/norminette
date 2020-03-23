from rules import Rule
from lexer import Lexer, TokenError

types = [
    "STRUCT",
    "ENUM",
    "UNION",
    "INT",
    "VOID",
    "CHAR",
    "UNSIGNED",
    "CONST",
    "DOUBLE",
    "LONG",
    "SHORT",
    "STATIC",
    "IDENTIFIER",
    "SPACE",
    "TAB"
]

class CheckTypedefDeclaration(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsUserDefinedType"]

    def run(self, context):
        i = 0
        i = context.skip_ws(i)
        tkns = context.tokens

        if tkns[i].type != "TYPEDEF":
            return False, 0
        i += 1
        i = context.skip_ws(i)
        while tkns[i].type in types:
            if context.check_token(i, "IDENTIFIER"):
                last_identifier = tkns[i]
            i += 1
        if context.check_token(i, "LBRACE") is True:
            i = context.skip_nest(i)
            i += 1
        while tkns[i].type in types:
            if tkns[i].type == "IDENTIFIER":
                last_identifier = tkns[i]
            i += 1
        if last_identifier.value.startswith("t_") is False:
            context.new_error("USER_DEFINED_TYPEDEF", last_identifier)
        if context.check_token(i, "SEMI_COLON") is False:
            context.new_error(1024, context.peek_token(i))
        i += 1
        token = context.peek_token(i)
        if token is not None and token.type != "NEWLINE":
            context.new_error(1024, token)
        return False, i
