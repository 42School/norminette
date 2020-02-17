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

    def check_arg_format(self, context, pos):
        i = self.skip_ws(context, pos)
        if context.peek_token(i) is not None \
                and context.peek_token(i).type == "VOID":
            i += 1
            i = self.skip_ws(context, i)
            if context.peek_token(i) is not None \
                    and context.peek_token(i).type == "RPARENTHESIS":
                return i
        i = self.skip_ws(context, pos)
        ret, i = self.skip_type_prefix(context, i)
        while context.peek_token(i) is not None \
                and context.check_token(i, ["MULT"] + whitespaces):
            i += 1
        stop = ["COMMA", "RPARENTHESIS"]
        if ret is True:
            if context.peek_token(i) is not None \
                    and context.peek_token(i).type != "IDENTIFIER":
                context.new_error(1016, context.peek_token(i - 1))
            else:
                i += 1
                i = self.skip_ws(context, i)
                while context.peek_token(i) is not None \
                        and context.peek_token(i).type not in stop:
                    i += 1
        else:
            context.new_error(1016, context.peek_token(i - 1))
        return i

    def no_arg_func(self, context, pos):
        pass

    def check_args(self, context, pos):
        i = pos
        while context.peek_token(i) is not None \
                and context.peek_token(i).type != "IDENTIFIER":
            i += 1
        while context.peek_token(i) is not None \
                and context.peek_token(i).type != "LPARENTHESIS":
            i += 1
        i += 1
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
        ret, pos = self.skip_type_prefix(context, 0)
        pos = self.skip_ws(context, pos)
        self.check_args(context, pos)
        return False, 0
