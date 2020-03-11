from lexer import Token
from rules import Rule
from rules.is_func_declaration import IsFuncDeclaration


type_specifiers = [
    "CHAR",
    "DOUBLE",
    "ENUM",
    "FLOAT",
    "INT",
    "UNION",
    "VOID"
]

misc_specifiers = [
    "CONST",
    "REGISTER",
    "STATIC",
    "STRUCT",
    "VOLATILE"
]

size_specifiers = [
    "LONG",
    "SHORT"
]

sign_specifiers = [
    "SIGNED",
    "UNSIGNED"
]

whitespaces = [
    "SPACE",
    "TAB",
    "NEWLINE"
]


class CheckEmptyFuncParams(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = [IsFuncDeclaration]

    def run(self, context):
        i = context.arg_pos[0] + 1
        i = context.skip_ws(i)
        if context.check_token(i, "VOID") is False \
                and context.check_token(i, "RPARENTHESIS") is True:
            context.new_error(1015, context.peek_token(i))
        return False, 0
