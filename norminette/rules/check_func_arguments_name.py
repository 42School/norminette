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
        self.depends_on = ["IsFuncDeclaration", "IsFuncPrototype"]

    def check_arg_format(self, context, pos):
        """
        A valid argument contains either:
        - a type specifier AND a paramater name (IDENTIFIER)
        - an ellipsis
        """

        i = context.skip_ws(pos)
        stop = ["COMMA", "RPARENTHESIS"]
        if context.check_token(i, ["COMMENT", "MULT_COMMENT"]):
            context.new_error("WRONG_SCOPE_COMMENT", context.peek_token(i))
            i += 1
        if context.check_token(i, "NEWLINE"):
            context.new_error("NEWLINE_IN_DECL", context.peek_token(i))
            i += 1
        if context.check_token(i, "ELLIPSIS"):
            i += 1
            if context.peek_token(i).type in stop:
                i += 1
            return i
        ret, i = context.check_type_specifier(i)
        while context.peek_token(i) is not None \
                and context.check_token(i, ["MULT"] + whitespaces):
            i += 1

        if ret is True:
            i = context.skip_misc_specifier(i)
            ret, i = context.check_identifier(i)
            if ret is False:
                context.new_error("MISSING_IDENTIFIER", context.peek_token(i - 1))
            else:
                i += 1
                i = context.skip_ws(i)

            while context.peek_token(i) is not None and i < context.arg_pos[1] \
                    and context.peek_token(i).type not in stop:
                if context.peek_token(i).type == "LPARENTHESIS":
                    i = context.skip_nest(i)
                i += 1
            i += 1

        else:
            while context.peek_token(i) is not None \
                    and context.peek_token(i).type not in stop:
                i += 1
            i += 1
        return i

    def no_arg_func(self, context, pos):
        i = context.skip_ws(pos)
        if context.check_token(i, "VOID"):
            i += 1
            i = context.skip_ws(i)
            if context.check_token(i, "RPARENTHESIS"):
                return True
        elif context.check_token(i, "RPARENTHESIS"):
            context.new_error("NO_ARGS_VOID", context.peek_token(i))
            return True
        return False

    def run(self, context):
        """
            Empty functions arguments must use void
        """
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
