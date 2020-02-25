from lexer import Token
from rules import Rule

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

arg_separator = [
    "COMMA",
    "CLOSING_PARENTHESIS"
]


class CheckFuncArgumentsName(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["CheckFuncDeclarations"]

    def skip_ws(self, context, pos):
        i = pos
        while context.peek_token(i) is not None \
                and context.peek_token(i).type in whitespaces:
            i += 1
        return i

    def check_arg_format(self, context, pos):
        i = self.skip_ws(context, pos)
        if context.check_token(i, "VOID"):
            i += 1
            i = self.skip_ws(context, i)
            if context.check_token(i, "RPARENTHESIS"):
                return i
        elif context.check_token(i, "ELLIPSIS"):
            i += 1
            return i
        i = self.skip_ws(context, pos)
        ret, i = self.check_type_specifier(context, i)
        while context.peek_token(i) is not None \
                and context.check_token(i, ["MULT"] + whitespaces):
            i += 1
        stop = ["COMMA", "RPARENTHESIS"]
        if ret is True:
            if context.check_token(i, "IDENTIFIER"):
                context.new_error(1016, context.peek_token(i - 1))
            else:
                i += 1
                i = self.skip_ws(context, i)
                while context.peek_token(i) is not None \
                        and context.peek_token(i).type not in stop:
                    i += 1
        else:
            print("here", context.tokens[:i], context.tokens[i])
            context.new_error(1016, context.peek_token(i - 1))
        return i

    def no_arg_func(self, context, pos):
        pass

    def check_args(self, context, pos):
        i = self.skip_ws(context, pos)
        while context.check_token(i, "IDENTIFIER") is False:
            i += 1
        while context.check_token(i, "LPARENTHESIS") is False:
            i += 1
        i += 1
        if context.check_token(i, "RPARENTHESIS"):
            return
        p = 1
        while p > 0 and context.peek_token(i) is not None:
            if context.peek_token(i).type == "LPARENTHESIS":
                p += 1
                while p:
                    if context.peek_token(i) is not None:
                        if context.peek_token(i).type == "LPARENTHESIS":
                            p += 1
                        elif context.peek_token(i).type == "RPARENTHESIS":
                            p -= 1
                    else:
                        break
                    i += 1
            elif context.peek_token(i).type == "RPARENTHESIS":
                p -= 1
                i += 1
            elif context.peek_token(i).type == "COMMA":
                i += 1
            else:
                i = self.check_arg_format(context, i)

    def run(self, context):
        ret, pos = self.check_type_specifier(context, 0)
        self.check_args(context, pos)
        return False, 0
