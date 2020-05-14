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

utypes = [
    "STRUCT",
    "ENUM",
    "UNION"
]

class CheckTypedefDeclaration(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsUserDefinedType"]

    def run(self, context):
        return False, 0
        i = 0
        i = context.skip_ws(i)
        tkns = context.tokens

        if context.check_token(i, "TYPEDEF") is False:
            return False, 0
        i += 1
        if context.check_token(i, "SPACE") is False:
            context.new_error("TAB_REPLACE_SPACE", context.peek_token(i))
        i += 1
        while context.check_token(i, utypes) is False:
            i += 1
        i += 1
        if context.check_token(i, "SPACE") is False:
            context.new_error("TAB_REPLACE_SPACE", context.peek_token(i))
        i += 1
        last_identifier = None
        if context.check_token(i, "IDENTIFIER"):
            last_identifier = tkns[i]
        i += 1
        i = context.skip_ws(i, nl=True)
        if context.check_token(i, "LBRACE") is True:
            i = context.skip_nest(i)
            i += 1
        while tkns[i].type in types:
            if tkns[i].type == "IDENTIFIER":
                last_identifier = tkns[i]
            i += 1
        if last_identifier is None:
            return False, 0
        if last_identifier.value.startswith("t_") is False:
            context.new_error("USER_DEFINED_TYPEDEF", last_identifier)
        tmp = i - 2
        while context.check_token(tmp, "TAB") is True:
            tmp -= 1
        if context.check_token(tmp, "SPACE") is True:
            context.new_error("SPACE_REPLACE_TAB", context.peek_token(tmp))
        if context.check_token(i, "SEMI_COLON") is False:
            context.new_error("TOO_MANY_INSTR", context.peek_token(i))
        i += 1
        token = context.peek_token(i)
        if token is not None and token.type != "NEWLINE":
            context.new_error("TOO_MANY_INSTR", token)
        return False, i
