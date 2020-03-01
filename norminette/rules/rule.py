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

    def skip_nest(self, context, pos):
        rbrackets = ["RBRACKET", "RBRACE", "RPARENTHESIS"]
        lbrackets = ["LBRACKET", "LBRACE", "LPARENTHESIS"]
        c = context.peek_token(pos).type
        if c not in lbrackets:
            return pos
        c = rbrackets[lbrackets.index(c)]
        i = pos + 1
        while context.peek_token(i) is not None:
            if context.check_token(i, lbrackets) is True:
                i = self.skip_nest(context, i)
                if i == -1:
                    return -1
            elif context.check_token(i, rbrackets) is True:
                if c == context.peek_token(i).type:
                    return i
                # raise nesting error?
                return -1
            i += 1
        return -1

    def skip_misc_specifier(self, context, pos):
        i = self.skip_ws(context, pos)
        if context.check_token(i, misc_specifiers):
            i += 1
            i = self.skip_ws(context, i)
        return i

    def check_type_specifier(self, context, pos):
        i = self.skip_misc_specifier(context, pos)

        if context.check_token(i, sign_specifiers):
            i += 1
            i = self.skip_misc_specifier(context, i)
            if context.check_token(i, size_specifiers):
                i += 1
                i = self.skip_misc_specifier(context, i)
                if context.check_token(i, type_specifiers):
                    i += 1
                    i = self.skip_misc_specifier(context, i)
                    return True, i
                return True, i
            return True, i

        if context.check_token(i, size_specifiers):
            i += 1
            i = self.skip_misc_specifier(context, i)
            if context.check_token(i, type_specifiers):
                i += 1
                i = self.skip_misc_specifier(context, i)
                return True, i
            return True, i

        if context.check_token(i, ["STRUCT", "ENUM", "UNION"]):
            i += 1
            i = self.skip_misc_specifier(context, i)
            if context.check_token(i, "IDENTIFIER"):
                i += 1
                return True, i
            return False, 0

        if context.check_token(i, type_specifiers + ["IDENTIFIER"]):
            i += 1
            i = self.skip_misc_specifier(context, i)
            return True, i

        return False, pos

    def check_identifier(self, context, pos):
        i = pos
        while context.check_token(i, whitespaces + ["MULT"]):
            i += 1
        if context.check_token(i, "IDENTIFIER"):
            return True, i
        return False, pos

    def skip_brackets(self, context, pos):
        i = self.skip_ws(context, pos)
        if context.check_token(i, "LBRACKET") is True:
            b = 1
            i += 1
            while b:
                if context.check_token(i, "LBRACKET"):
                    b += 1
                elif context.check_token(i, "RBRACKET"):
                    b -= 1
                i += 1
        return i


class PrimaryRule(Rule):
    def __init__(self):
        super().__init__()
        self.primary = True
        self.priority = 0
