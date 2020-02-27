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

    def skip_nested_par(self, context, pos):
        i = pos + 1
        while context.peek_token(i).type != "RPARENTHESIS":
            if context.peek_token(i).type == "LPARENTHESIS":
                i = self.skip_nested_par(context, i)
            i += 1
        return i

    def check_arg_format(self, context, pos):
        """
        A valid argument contains either:
        - a type specifier AND a paramater name (IDENTIFIER)
        - an ellipsis
        """

        i = self.skip_ws(context, pos)
        stop = ["COMMA", "RPARENTHESIS"]

        if context.check_token(i, "ELLIPSIS"):
            i += 1
            return i

        ret, i = self.check_type_specifier(context, i)
        while context.peek_token(i) is not None \
                and context.check_token(i, ["MULT"] + whitespaces):
            i += 1

        if ret is True:
            i = self.skip_misc_specifier(context, i)
            ret, i = self.check_identifier(context, i)
            if ret is False:
                context.new_error(1016, context.peek_token(i - 1))
            else:
                i += 1
                i = self.skip_ws(context, i)
            while i < context.arg_pos[1] \
                    and context.peek_token(i).type not in stop:
                if context.peek_token(i).type == "LPARENTHESIS":
                    i = self.skip_nested_par(context, i)
                i += 1
            i += 1
        else:
            while context.peek_token(i) is not None \
                    and context.peek_token(i).type not in stop:
                i += 1
            i += 1
        return i

    def no_arg_func(self, context, pos):
        i = self.skip_ws(context, pos)
        if context.check_token(i, "VOID"):
            i += 1
            i = self.skip_ws(context, i)
            if context.check_token(i, "RPARENTHESIS"):
                return True
        elif context.check_token(i, "RPARENTHESIS"):
            return True
        return False

    def run(self, context):
        i = context.arg_pos[0] + 1
        ret = self.no_arg_func(context, i)
        if ret is True:
            return False, 0
        while i < context.arg_pos[1]:
            if context.peek_token(i).type == "LPARENTHESIS":
                p = 1
                while p:
                    if context.peek_token(i) is not None:
                        if context.peek_token(i).type == "LPARENTHESIS":
                            p += 1
                        elif context.peek_token(i).type == "RPARENTHESIS":
                            p -= 1
                    else:
                        break
                    i += 1
            else:
                i = self.check_arg_format(context, i)
        return False, 0
