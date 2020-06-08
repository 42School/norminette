from lexer import Token
from rules import PrimaryRule
from context import GlobalScope, Function

whitespaces = ["SPACE", "TAB"]
assigns = [
    "RIGHT_ASSIGN",
    "LEFT_ASSIGN",
    "ADD_ASSIGN",
    "SUB_ASSIGN",
    "MUL_ASSIGN",
    "DIV_ASSIGN",
    "MOD_ASSIGN",
    "AND_ASSIGN",
    "XOR_ASSIGN",
    "OR_ASSIGN",
    "ASSIGN",
]
misc_identifier = [
    "CONST",
    "REGISTER",
    "STATIC",
    "VOLATILE",
    "EXTERN",
    "INLINE",
    "RESTRICT",
    "SIGNED",
    "UNSIGNED",
    "LONG",
    "SHORT",
    "TYPEDEF",
    "STRUCT",
    "ENUM",
    "UNION"
]
type_identifier = [
    "CHAR",
    "DOUBLE",
    "ENUM",
    "FLOAT",
    "INT",
    "UNION",
    "VOID",
    "LONG",
    "SHORT",
]
class IsFuncDeclaration(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 11
        self.scope = [GlobalScope]

    def check_args(self, context, pos):
        i = context.skip_ws(pos, nl=True)
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
        i = context.skip_ws(pos, nl=True)
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
        i = context.skip_misc_specifier(i, nl=True)
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
        i = context.skip_ws(0, nl=False)
        type_id = []
        misc_id = []
        identifier = None
        args = False
        if context.check_token(i, "NEWLINE") is True:
            return False, 0
        while context.peek_token(i) and context.check_token(i, "NEWLINE") is False:
            if context.check_token(i, misc_identifier) is True:
                misc_id.append(context.peek_token(i))
            elif context.check_token(i, type_identifier) is True:
                type_id.append(context.peek_token(i))
            if context.check_token(i, assigns) is True:
                return False, 0
            elif context.check_token(i, "IDENTIFIER") is True:
                if identifier is not None:
                    type_id.append(identifier[0])
                identifier = (context.peek_token(i), i)
            if context.check_token(i, "LPARENTHESIS") is True:
                par = context.parenthesis_contain(i)
                if par[0] == "function":
                    if identifier is not None:
                        type_id.append(identifier[0])
                    identifier = (context.peek_token(i), i)
                    i = context.skip_nest(i)
                else:
                    args = True
                    arg_start = i
                    i = context.skip_nest(i)
                    arg_end = i
            else:
                i += 1
        if len(type_id) > 0 and args == True:
            i = identifier[1]
            while context.check_token(i, ["LPARENTHESIS", "MULT", "BWISE_AND"]) is True:
                i += 1
            context.scope.fnames.append(context.peek_token(i).value)
            context.fname_pos = i
            context.arg_pos = [arg_start, arg_end]
            i += 1
            while context.check_token(i, ["RPARENTHESIS"]) is True:
                i += 1
            i = context.skip_nest(i)
            return True, i + 1
        return False, 0
        #ret, i = context.check_type_specifier(i, nl=True)
        """if ret is False:
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
"""
        return True, i

    def run(self, context):

        if type(context.scope) is not GlobalScope:
            return False, 0

        ret, read = self.check_func_format(context)
        if ret is False:
            return False, 0
        if context.check_token(read, ["NEWLINE", "LBRACE"]):
            if context.check_token(read, ["LBRACE"]) is True:
                read -= 2
            context.scope.functions += 1
            read += 1
            context.sub = context.scope.inner(Function)
            read = context.eol(read)
            return True, read

        elif context.check_token(read, "SEMI_COLON"):
            read += 1
            read = context.eol(read)
            return False, 0

        return False, 0
