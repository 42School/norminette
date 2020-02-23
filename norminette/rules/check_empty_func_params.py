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


class CheckEmptyFuncParams(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["CheckFuncDeclarations"]

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
                return True, i

            else:
                return True, i
        elif context.peek_token(i) is not None \
                and context.peek_token(i).type in size_specifiers:
            i += 1
            i = self.skip_ws(context, i)
            if context.peek_token(i).type is not None \
                    and context.peek_token(i) in type_specifiers:
                return True, i
            return True, i
        elif context.peek_token(i) is not None \
                and (
                    context.peek_token(i).type in type_specifiers
                    or context.peek_token(i).type == "IDENTIFIER"):
            i += 1
            return True, i
        else:
            i += 1
            return False, i

    def run(self, context):
        ret, i = self.skip_type_prefix(context, 0)
        i = self.skip_ws(context, i)
        while context.peek_token(i) is not None \
                and context.peek_token(i).type != "IDENTIFIER":
            i += 1
        while context.peek_token(i) is not None \
                and context.peek_token(i).type != "LPARENTHESIS":
            i += 1
        i += 1
        i = self.skip_ws(context, i)
        if context.peek_token(i) is not None \
                and context.peek_token(i).type == "RPARENTHESIS":
            context.new_error(1015, context.peek_token(i))

        return False, 0
