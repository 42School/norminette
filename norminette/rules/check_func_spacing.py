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
    def skip_ws(self, context, pos):
        i = pos
        while context.peek_token(i) is not None \
                and context.peek_token(i).type in whitespaces:
            i += 1
        return i

    def skip_type_prefix(self, context, pos):
        i = pos
        i = self.skip_ws(context, i)

        if context.peek_token(i) is not None \
                and context.peek_token(i).type in misc_specifiers:
            # Skipping "const/register/struct/static/volatile" keywords
            i += 1
            i = self.skip_ws(context, i)

        if context.peek_token(i) is not None \
                and context.peek_token(i).type in sign_specifiers:
            # This case is the 'trickier'
            # sign specifier (signed, unsigned) can be followed by:
            # optionnal size specifier (long, short)
            # AND/OR optionnal type specifier (int, char)
            i += 1
            i = self.skip_ws(context, i)
            if context.peek_token(i) is not None \
                    and context.peek_token(i).type in size_specifiers:
                i += 1
                i = self.skip_ws(context, i)
                if context.peek_token(i) is not None \
                        and context.peek_token(i).type in type_specifiers:
                    i += 1
                    i = self.skip_ws(context, i)
                    return i
                return i

            else:
                return i
        elif context.peek_token(i) is not None \
                and context.peek_token(i).type in size_specifiers:
            i += 1
            i = self.skip_ws(context, i)
            if context.peek_token(i).type is not None \
                    and context.peek_token(i) in type_specifiers:
                return i
            return i

        else:
            i += 1
            return i

    def trim_newlines(self, context):
        i = 0
        line = 0
        while i < context.tkn_scope and context.peek_token(i) is not None \
                and context.peek_token(i).type not in misc_specifiers \
                and context.peek_token(i).type not in size_specifiers \
                and context.peek_token(i).type not in sign_specifiers \
                and context.peek_token(i).type not in type_specifiers:
            if context.peek_token(i).type == "NEWLINE":
                line = i + 1
            i += 1
        return line

    def run(self, context):
        start = self.trim_newlines(context)
        i = self.skip_type_prefix(context, start)
        if context.peek_token(i).type == "SPACE":
            context.new_error(1010, context.peek_token(i))
        return False, 0
