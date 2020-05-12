from rules import Rule
from scope import *

kw = [
    # C reserved keywords #
    "AUTO",
    "BREAK",
    "CASE",
    "CHAR",
    "CONST",
    "CONTINUE",
    "DEFAULT",
    "DO",
    "DOUBLE",
    "ELSE",
    "ENUM",
    "EXTERN",
    "FLOAT",
    "FOR",
    "GOTO",
    "IF",
    "INT",
    "LONG",
    "REGISTER",
    "RETURN",
    "SHORT",
    "SIGNED",
    "STATIC",
    "STRUCT",
    "SWITCH",
    "TYPEDEF",
    "UNION",
    "UNSIGNED",
    "VOID",
    "VOLATILE",
    "WHILE"
]

class CheckExpressionStatement(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsExpressionStatement", "IsControlStatement"]

    def run(self, context):
        i = 0
        while context.check_token(i, ["SEMI_COLON", "NEWLINE"]) is False:
            if context.check_token(i, kw) is True:
                if context.check_token(i + 1, "SPACE") is False:
                    context.new_error("SPACE_AFTER_KW", context.peek_token(i))
                    return False, 0
            if context.check_token(i, "RETURN") is True:
                tmp = i
                while context.check_token(tmp, "SEMI_COLON") is False:
                    if context.check_token(tmp, "LPARENTHESIS") is True:
                        return False, 0
                    tmp += 1
                if context.check_token(tmp, "SEMI_COLON") is True:
                    if context.check_token(tmp - 1, "SPACE") is False and context.check_token(tmp - 2, "RETURN") is False:
                        context.new_error("RETURN_PARENTHESIS", context.peek_token(tmp))
                    return False, 0
            i += 1
        return False, 0
