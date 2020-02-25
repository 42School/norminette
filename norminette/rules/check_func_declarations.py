from lexer import Token
from rules import Rule

type_specifiers = ["CHAR", "DOUBLE", "ENUM", "FLOAT", "INT", "UNION", "VOID"]

misc_specifiers = ["CONST", "REGISTER", "STATIC", "VOLATILE"]

size_specifiers = ["LONG", "SHORT"]

sign_specifiers = ["SIGNED", "UNSIGNED"]

all_types = type_specifiers + size_specifiers + sign_specifiers \
            + misc_specifiers

whitespaces = ["NEWLINE", "SPACE", "TAB"]


class CheckFuncDeclarations(Rule):
    def __init__(self):
        super().__init__()
        self.primary = True

    def check_args(self, context, pos):
        i = self.skip_ws(context, pos)
        while context.check_token(i, whitespaces + ["RPARENTHESIS"]):
            i += 1
        if context.check_token(i, "LPARENTHESIS") is False:
            return False, pos
        p = 1
        i += 1
        while p:
            if context.check_token(i, "LPARENTHESIS"):
                p += 1
            elif context.check_token(i, "RPARENTHESIS"):
                p -= 1
            elif context.peek_token(i) is None:
                return False, 0
            i += 1
        return True, i

    def check_func_identifier(self, context, pos):
        i = self.skip_ws(context, pos)
        pp = 0  # Pointer operator's position
        lp = 0  # Left parenthesis counter (nesting level)

        if context.check_token(i, "IDENTIFIER"):
            i += 1
            return True, i, False

        d = ["LPARENTHESIS", "MULT"] + whitespaces
        while context.check_token(i, d):
            if context.check_token(i, "MULT") and not pp:
                pp = i
            elif pp and context.check_token(i, "LPARENTHESIS"):
                lp += 1
            i += 1
        if context.check_token(i, "IDENTIFIER") is False:
            return False, pos, False

        i += 1
        while context.check_token(i, ["RPARENTHESIS"] + whitespaces):
            if context.check_token(i, "RPARENTHESIS"):
                lp -= 1
            i += 1
        if pp and lp < 0 and context.check_token(i, "LPARENTHESIS"):
            return False, pos, False

        return True, i, (True if pp else False)

    def check_func_format(self, context):
        i = self.skip_ws(context, 0)
        ret, i = self.check_type_specifier(context, i)
        if ret is False:
            return False, 0
        ret, i, fp = self.check_func_identifier(context, i)
        if ret is False:
            return False, 0

        ret, i = self.check_args(context, i)
        if ret is False:
            return False, 0

        if fp is True:
            ret, i = self.check_args(context, i)

        while context.check_token(i, ["RPARENTHESIS"] + whitespaces):
            i += 1

        return True, i

    def run(self, context):

        if context.global_scope is False:
            return False, 0

        ret, read = self.check_func_format(context)
        if ret is False:
            return False, 0

        if context.check_token(read, "LBRACE"):
            context.functions_declared += 1
            return True, read

        elif context.check_token(read, "SEMI_COLON"):
            read += 1
            return True, read

        return False, 0
