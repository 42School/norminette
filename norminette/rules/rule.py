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

    def skip_nested_par(self, context, pos):
        i = pos + 1
        while context.peek_token(i).type != "RPARENTHESIS":
            if context.peek_token(i).type == "LPARENTHESIS":
                i = self.skip_nested_par(context, i)
            i += 1
        return i

    def skip_nested_brace(self, context, pos):
        i = pos + 1
        while context.peek_token(i).type != "RBRACE":
            if context.peek_token(i).type == "LBRACE":
                i = self.skip_nested_brace(context, i)
            i += 1
        return i

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
        while context.check_token(i, whitespaces + ["MULT", "LPARENTHESIS"]):
            i += 1
        if context.check_token(i, "IDENTIFIER"):
            return True, i
        return False, pos


class PrimaryRule(Rule):
    def __init__(self):
        super().__init__()
        self.primary = True
        self.priority = 0
