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


class Rule:
    def __init__(self):
        self.name = type(self).__name__
        self.dependencies = []
        self.primary = False

    def skip_ws(self, context, pos):
        while context.check_token(pos, ["TAB", "SPACE", "NEWLINE"]):
            pos += 1
        return pos

    def check_sign_specifier(self, context, pos):
        i = pos
        i = self.skip_ws(context, i)
        if context.check_token(i, sign_specifiers):
            i += 1
            ret, i = self.check_size_specifier(context, i)
            if ret is True:
                return True, i
            return self.check_type_specifier(context, i)
        else:
            return False, pos

    def check_size_specifier(self, context, pos):
        i = pos
        i = self.skip_ws(context, i)
        if context.check_token(i, size_specifiers):
            i += 1
            return self.check_type_specifier(context, i)
        else:
            return False, pos
        pass

    def check_struct_prefix(self, context, pos):
        i = pos
        pass

    def check_type_specifier(self, context, pos):
        i = pos
        i = self.skip_ws(context, i)
        if context.check_token(i, type_specifiers):
            i += 1
            return True, i
        elif context.check_token(i, "IDENTIFIER"):
            i += 1
            return True, i
        else:
            return False, pos
