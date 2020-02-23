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
        self.depends_on = []
        self.primary = False

    def register(self, registry):
        for rule in self.depends_on:
            if rule in registry.dependencies:
                registry.dependencies[rule].append(self.name)
            else:
                registry.dependencies[rule] = [self.name]

    def skip_ws(self, context, pos):
        while context.check_token(pos, ["TAB", "SPACE", "NEWLINE"]):
            pos += 1
        return pos

    def check_type_specifier(self, context, pos):
        i = self.skip_ws(context, pos)

        if context.check_token(i, misc_specifiers):
            i += 1
            i = self.skip_ws(context, i)

        if context.check_token(i, sign_specifiers):
            i += 1
            i = self.skip_ws(context, i)
            if context.check_token(i, size_specifiers):
                i += 1
                i = self.skip_ws(context, i)
                if context.check_token(i, type_specifiers):
                    i += 1
                    return True, i
                return True, i
            return True. i

        if context.check_token(i, sign_specifiers):
            i += 1
            i = self.skip_ws(context, i)
            if context.check_token(i,sign_specifiers):
                i += 1
                return True. i
            return True, i

        if context.check_token(i, type_specifiers + ["IDENTIFIER"]):
            i += 1
            return True, i

        return False, pos
