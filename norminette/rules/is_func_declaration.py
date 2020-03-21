from lexer import Token
from rules import PrimaryRule
from context import GlobalScope, Function

whitespaces = ["NEWLINE", "SPACE", "TAB"]


class IsFuncDeclaration(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 10
        self.scope = [GlobalScope]

    def check_args(self, context, pos):
        i = context.skip_ws(pos)
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
        i = context.skip_ws(pos)
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
        i = context.skip_misc_specifier(i)
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
        i = context.skip_ws(0)
        ret, i = context.check_type_specifier(i)
        if ret is False:
            return False, 0

        name_pos = i
        ret, i, fp = self.check_func_identifier(context, i)
        if ret is False:
            return False, 0

        arg_start = i
        while context.peek_token(name_pos).type != "IDENTIFIER":
            name_pos += 1
        ret, i = self.check_args(context, i)
        if ret is False:
            return False, 0

        if fp is True:
            ret, i = self.check_args(context, i)
        arg_end = i
        context.scope.fnames.append(context.peek_token(name_pos).value)
        context.fname_pos = name_pos
        context.arg_pos = [arg_start, arg_end]

        while context.check_token(i, ["RPARENTHESIS"] + whitespaces):
            i += 1

        return True, i

    def run(self, context):

        if type(context.scope) is not GlobalScope:
            return False, 0

        ret, read = self.check_func_format(context)
        if ret is False:
            return False, 0

        if context.check_token(read, "LBRACE"):
            context.scope.functions += 1
            read += 1
            context.sub = context.scope.inner(Function)
            read = context.eol(read)
            return True, read

        elif context.check_token(read, "SEMI_COLON"):
            read += 1
            read = context.eol(read)
            return True, read

        return False, 0
