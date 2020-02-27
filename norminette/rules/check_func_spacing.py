from rules import Rule

whitespaces = [
    "SPACE",
    "TAB",
    "NEWLINE"
]

type_specifiers = [
    "CHAR",
    "DOUBLE",
    "ENUM",
    "FLOAT",
    "INT",
    "UNION",
    "VOID",
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

arg_separator = [
    "COMMA",
    "CLOSING_PARENTHESIS"
]


class CheckFuncSpacing(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["CheckFuncDeclarations"]


    def run(self, context):
        i = context.fname_pos - 1
        if context.peek_token(i).type == "SPACE":
            context.new_error(1010, context.peek_token(i))
        if context.peek_token(i).type == "TAB":
            j = i
            while context.peek_token(j).type == "TAB":
                j -= 1
            if j + 1 < i:
                context.new_error(1011, context.peek_token(i))
            if context.peek_token(i).type == "SPACE":
                context.new_error(1010, context.peek_token(i))
        else:
            context.new_error(1012, context.peek_token(i))
        return False, 0
