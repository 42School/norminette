from lexer import Token
from rules import Rule

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


class CheckVarDeclarations(Rule):
    def __init__(self):
        super().__init__()
        self.dependencies = []
        self.primary = True

    def skip_ws(self, context, pos):
        i = pos
        while context.peek_token(i) is not None \
                and context.peek_token(i).type in whitespaces:
            i += 1
        return i

    def check_struct_prefix(self, context, pos):
        i = pos
        if context.peek_token(i) is not None \
                and context.peek_token(i).type == "":
            i += 1
            i = self.skip_ws(context, i)
            if context.peek_token(i) is not None \
                    and context.peek_token(i).type == "IDENTIFIER":
                i += 1
                i = self.skip_ws(context, i)
                if context.peek_token(i) is not None \
                        and context.peek_token(i).type == "IDENTIFIER":
                    i += 1
                    i = self.skip_ws(context, pos)
                    return True, i
                return True, i

        return False, pos

    def check_sign_prefix(self, context, pos):
        i = pos
        if context.peek_token(i) is not None \
                and context.peek_token(i).type in sign_specifiers:
            i += 1
            i = self.skip_ws(context, pos)
            if context.peek_token(i) is not None \
                    and context.peek_token(i).type in size_specifiers:
                i += 1
                i = self.skip_ws(context, pos)
                if context.peek_token(i) is not None \
                        and (
                            context.peek_token(i).type in type_specifiers
                            or context.peek_token(i).type == "IDENTIFIER"):
                    i += 1
                    i = self.skip_ws(context, pos)
                    return True, i
                return True, i

        return False, pos

    def check_type_prefix(self, context, pos):
        i = self.skip_ws(context, pos)

        if context.peek_token(i) is not None \
                and context.peek_token(i).type in sign_specifiers:
            i += 1
            i = self.skip_ws(context, i)

        ret, i = self.check_struct_prefix(context, i)
        if ret is True:
            return ret, i

        ret, i = p

        pass

    def run(self, context):
        return False, 0
        pass
