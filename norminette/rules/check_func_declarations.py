from .norm_error import NormError

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

whitespaces = [
    "SPACE",
    "TAB",
    "NEWLINE"
]

arg_separator = [
    "OP_COMMA",
    "CLOSING_PARENTHESIS"
]


class CheckFuncDeclarations:
    def __init__(self):
        self.name = "CheckFuncDeclaration"
        self.__i = 0

    def skip_ws(self, context, pos):
        i = 0
        while context.peekToken(pos + i) is not None \
                and context.peekToken(pos + i).type in whitespaces:
            i += 1
        return i

    def skip_opening_parenthesis(self, context, pos):
        i = 0
        while context.peekToken(pos + i) is not None \
                and i < stop:
            if context.peekToken(pos + i).type == "OPENING_PARENTHESIS":
                i += 1
            elif context.peekToken(pos + i).type in whitespaces:
                pos += 1
        return i

    def skip_closing_parenthesis(self, context, pos, stop):
        i = 0
        while context.peekToken(pos + i) is not None \
                and i < stop:
            if context.peekToken(pos + i).type == "CLOSING_PARENTHESIS":
                i += 1
            elif context.peekToken(pos + i).type in whitespaces:
                pos += 1
        return i

    def check_type_prefix(self, context, pos):
        i = pos
        i += self.skip_ws(context, i)

        if context.peekToken(i) is not None \
                and context.peekToken(i).type in misc_specifiers:
            # Skipping "const/register/struct/static/volatile" keywords
            i += 1
            i += self.skip_ws(context, i)

        if context.peekToken(i) is not None \
                and context.peekToken(i).type in sign_specifiers:
            # This case is the 'trickier'
            # sign specifier (signed, unsigned) can be followed by:
            # optionnal size specifier (long, short)
            # AND/OR optionnal type specifier (int, char)
            i += 1
            i += self.skip_ws(context, i)
            if context.peekToken(i) is not None \
                    and context.peekToken(i).type in size_specifiers:
                i += 1
                i += self.skip_ws(context, i)
                if context.peekToken(i) is not None \
                        and context.peekToken(i).type in type_specifiers:
                    i += 1
                    i += self.skip_ws(context, i)
                    return True, i
                return True, i

            else:
                i += 1
                return True, i
        elif context.peekToken(i) is not None \
                and context.peekToken(i).type in size_specifiers:
            i += 1
            i += self.skip_ws(context, i)
            if context.peekToken(i).type is not None \
                    and context.peekToken(i) in type_specifiers:
                return True, i
            return True, i
        elif context.peekToken(i) is not None \
                and (
                    context.peekToken(i).type in type_specifiers
                    or context.peekToken(i).type == "IDENTIFIER"):
            return True, i

        return False, pos

    def check_identifier_format(self, context, pos):
        i = pos
        pass

    def check_func_pointer_args(self, context, pos):
        pass

    def check_func_args(self, context, pos):
        pass

    def count_func_args(self, context, pos):
        return 0

    def check_func_prefix(self, context):
        i = self.skip_ws(context, 0)
        ret, jump = self.check_type_prefix(context, i)
        if ret is True:
            i += jump
            while context.peekToken(i) is not None \
                    and context.peekToken(i).type == "OP_MULT":
                i += 1
            return ret, i
        return False, 0

    def check_func_identifier(self, context, pos):
        i = pos
        i += self.skip_ws(context, i)
        if context.peekToken(i) is not None \
                and context.peekToken(i).type in [
                                                    "OP_MULT",
                                                    "OPENING_PARENTHESIS"]:
            i += 1
            ret, jump = self.check_func_identifier(self, context, i)
        elif context.peekToken(i) is not None \
                and context.peekToken(i).type == "CLOSING_PARENTHESIS":
                return True, i
                pass
        return False, pos

    def check_func_format(self, context):
        ret, jump = self.check_func_prefix(context)
        if ret is True:
            pos = jump
            ret, jump = self.check_func_identifier
        pass

    def run(self, context):
        self.__i += 1
        ret, jump = self.check_func_prefix(context)
        print(context.tokens, ret, jump)
        if ret is True:
            pos = jump
            return True, pos
        return False, 0
