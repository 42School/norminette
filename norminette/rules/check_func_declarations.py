from lexer import Token
from rules import Rule

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


class CheckFuncDeclarations(Rule):
    def __init__(self):
        super().__init__()
        self.primary = True

    def has_args(self, context, pos, ilvl):
        #arguments check is not correctly done
        i = self.skip_ws(context, pos)
        if context.check_token(i, "LPARENTHESIS") is False:
            return False, pos
        i += 1
        alvl = ilvl + 1
        while context.check_token(i, ["SEMI_COLON", "LBRACE"]) is False \
                and context.peek_token(i) is not None:
            if context.check_token(i, "LPARENTHESIS"):
                alvl += 1
            elif context.check_token(i, "RPARENTHESIS"):
                alvl -= 1
                if alvl == ilvl:
                    return True, i 
            i += 1
        else:
            return False, pos

    def returns_function_pointer(self, context, pos):
        i = pos
        i = self.skip_ws(context, i)
        if context.check_token(i, "LPARENTHESIS") is False:
            return False, pos
        i += 1
        ilvl = 1 #
        plvl = 0
        while context.check_token(
                i, ["LPARENTHESIS", "MULT"] + whitespaces):
            if context.check_token(i, "LPARENTHESIS"):
                ilvl += 1
            elif context.check_token(i, "MULT") and plvl == 0:
                plvl = ilvl
            i += 1
        if context.check_token(i, "IDENTIFIER") is False  or plvl == 0:
            return False, pos
        i += 1
        ret, i = self.has_args(context, i, plvl)
        #print(1, ret, context.tokens[:i])
        if ret is False:
            return False, pos
        i += 1
        ret, i = self.has_args(context, i, plvl)
        #print(2, ret, context.tokens[:i], plvl - 1)
        if ret is False:
            return False, pos
        while context.check_token(i, whitespaces + "RPARENTHESIS"):
            i += 1
        return True, i

    def is_function(self, context, pos):
        i = self.skip_ws(context, pos)
        ilvl = 0
        while context.check_token(i, ["MULT", "LPARENTHESIS"] + whitespaces):
            if context.check_token(i, "LPARENTHESIS"):
                ilvl += 1
            i += 1
        if context.check_token(i, "IDENTIFIER") is False:
            return False, pos
        i += 1
        ret, i = self.has_args(context, i, ilvl)
        while ilvl > 0:
            if context.check_token(i, "RPARENTHESIS"):
                ilvl -= 1
            i += 1
        # print("IS FUNC: after has_args -->",ret, i)
        return ret, (i if ret is True else pos)

    def check_func_prefix(self, context):
        i = self.skip_ws(context, 0)
        ret, i = self.check_functype_prefix(context, i)
        if ret is True:
            while context.check_token(i, "MULT"):
                i += 1
            return ret, i
        return False, 0


    def check_func_format(self, context):
        ret, i = self.check_type_specifier(context, 0)
        #print("out of prfix", ret, context.tokens[:i+1])
        if ret is False:
            return False, 0

        i = self.skip_ws(context, i)
        pos = 0
        if context.check_token(i, "LPARENTHESIS"):
            ret, pos = self.returns_function_pointer(context, i)
            #print("out of returns...", ret, context.tokens[:pos+1])
            if ret is False:
                ret, pos = self.is_function(context, i)
                #print("out of is_func...", ret, context.tokens[:pos+1])

        elif context.check_token(i, ["MULT", "IDENTIFIER"]):
            ret, pos = self.is_function(context, i)
            #print("Out of is_func...", ret, context.tokens[:pos+1])
            #        print(ret, i, context.tokens[:i])

        return ret, (pos if ret is True else 0)

    def run(self, context):
        ret, jump = self.check_func_format(context)

        if ret is False:
            return False, 0

        #print("Out of check_func_format...", ret, context.tokens[:jump + 1])
        jump = self.skip_ws(context, jump + 1)
        #print("Out of check_func_format...", ret, context.tokens[:jump + 1])


        if context.check_token(jump, "LBRACE"):
            context.functions_declared += 1
            return True, jump
            # print(context.tokens[:jump])
        elif context.check_token(jump, "SEMI_COLON"):
            while context.check_token(jump, "NEWLINE") is False:
                if context.check_token(jump, ["TAB", "SPACE"]) is False:
                    break
                jump += 1
            return True, jump

        return False, 0
