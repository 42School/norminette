from norminette.context import ControlStructure
from norminette.scope import Function
from norminette.context import GlobalScope
from norminette.scope import UserDefinedType
from norminette.rules import PrimaryRule


lbrackets = ["LBRACE", "LPARENTHESIS", "LBRACKET"]
rbrackets = ["RBRACE", "RPARENTHESIS", "RBRACKET"]

misc_specifiers = [
    "CONST",
    "REGISTER",
    "STATIC",
    "VOLATILE",
    "EXTERN",
    "INLINE",
    "RESTRICT" "SIGNED",
    "UNSIGNED",
]

type_specifiers = [
    "CHAR",
    "DOUBLE",
    "ENUM",
    "FLOAT",
    "INT",
    "UNION",
    "VOID",
    "LONG",
    "SHORT",
    "STRUCT",
    "ENUM",
    "UNION",
]


class IsVarDeclaration(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 75
        self.scope = [GlobalScope, UserDefinedType, Function, ControlStructure]

    def assignment_right_side(self, context, pos):
        sep = ["COMMA", "SEMI_COLON", "ASSIGN"]
        i = context.skip_ws(pos, nl=True)
        while context.peek_token(i) and context.check_token(i, sep) is False:
            if context.check_token(i, lbrackets) is True:
                i = context.skip_nest(i)
            i += 1
        return True, i

    def var_declaration(self, context, pos, identifier=False):
        pclose = ["RPARENTHESIS", "NEWLINE", "SPACE", "TAB"]
        brackets = 0
        parenthesis = 0
        braces = 0
        i = pos
        ret_store = None
        while context.peek_token(i) is not None and context.check_token(i, ["SEMI_COLON"]) is False:
            if context.check_token(i, "IDENTIFIER") is True and braces == 0 and brackets == 0 and parenthesis == 0:
                identifier = True
            elif context.check_token(i, ["COMMENT", "MULT_COMMENT"]) is True:
                i += 1
                continue
            elif context.check_token(i, ["COLON", "CONSTANT"]) is True and identifier == True:
                i += 1
                continue
            elif context.check_token(i, lbrackets) is True:
                if context.check_token(i, "LBRACE") is True:
                    braces += 1
                if context.check_token(i, "LBRACKET") is True:
                    brackets += 1
                if context.check_token(i, "LPARENTHESIS") is True:
                    ret, tmp = context.parenthesis_contain(i, ret_store)
                    if ret == "function" or ret == "pointer":
                        ret_store = ret
                        identifier = True
                        i = tmp
                    else:
                        parenthesis += 1
            elif context.check_token(i, rbrackets) is True:
                if context.check_token(i, "RBRACE") is True:
                    braces -= 1
                if context.check_token(i, "RBRACKET") is True:
                    brackets -= 1
                if context.check_token(i, "RPARENTHESIS") is True:
                    parenthesis -= 1
            elif context.check_token(i, "ASSIGN") is True:
                if identifier == False:
                    return False, pos
                ret, i = self.assignment_right_side(context, i + 1)
                i -= 1
                if ret is False:
                    return False, pos
            elif context.check_token(i, ["SPACE", "TAB", "MULT", "BWISE_AND", "NEWLINE"] + misc_specifiers + type_specifiers):
                pass
            elif context.check_token(i, "COMMA") is True and parenthesis == 0 and brackets == 0 and braces == 0:
                break
            elif parenthesis == 0 and brackets == 0 and braces == 0:
                return False, 0
            i += 1
        if identifier == False or braces > 0 or brackets > 0 or parenthesis > 0:
            return False, 0
        if context.check_token(i, "SEMI_COLON") is True:
            if brackets == 0 and braces == 0 and parenthesis == 0:
                return True, i
            else:
                return False, 0
        if context.check_token(i, "COMMA") is True:
            i += 1
            return True, i
        return False, pos

    def is_func_pointer(self, context, pos):
        i = context.skip_ws(pos)
        ws = ["SPACE", "TAB", "NEWLINE"]
        if context.check_token(i, "LPARENTHESIS") is False:
            return False, pos
        identifier = False
        i += 1
        p = 1
        plvl = 0  # nesting level of the first pointer operator encountered

        while p and context.check_token(i, ["MULT", "LPARENTHESIS"] + ws):
            if context.check_token(i, "MULT") and not plvl:
                plvl = p
            elif context.check_token(i, "LPARENTHESIS"):
                p += 1
            i += 1

        while p and context.peek_token(i) is not None:
            if context.check_token(i, "LPARENTHESIS") is True:
                p += 1
                if identifier is True:
                    return False, pos
            elif context.check_token(i, "RPARENTHESIS") is True:
                p -= 1
                if identifier is True:
                    par_pos = i
                    break
            elif context.check_token(i, "IDENTIFIER") is True:
                identifier = True
            i += 1
        else:
            return False, pos
        i += 1
        i = context.skip_nest(i)
        return True, i

    def run(self, context):
        """
        Catches all kinds of variable declarations
        """
        ret, i = context.check_type_specifier(0)
        if ret is False:
            return False, 0
        tmp = i - 1
        while context.check_token(tmp, ["LPARENTHESIS", "MULT", "BWISE_AND"]):
            tmp -= 1
        if context.check_token(tmp, "SEMI_COLON"):
            return True, i
        if (
            context.check_token(tmp, ["SPACE", "TAB", "NEWLINE"]) is False
            and context.check_token(tmp - 1, ["SPACE", "TAB", "NEWLINE"]) is False
        ):
            return False, 0
        ret, i = self.var_declaration(context, i)
        if ret is False:
            return False, 0
        while ret:
            if context.check_token(i, "SEMI_COLON") is False:
                ret, i = self.var_declaration(context, i)
            if context.check_token(i, "SEMI_COLON") is True:
                i += 1
                i = context.eol(i)
                return True, i
        return False, 0
