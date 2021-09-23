from norminette.context import ControlStructure
from norminette.scope import Function
from norminette.exceptions import CParsingError
from norminette.rules import PrimaryRule
import pdb
keywords = ["BREAK", "CONTINUE", "GOTO", "RETURN"]

operators = [
    "MULT",
    "LPARENTHESIS",
    "RPARENTHESIS",
    "LBRACKET",
    "RBRACKET",
    "PTR",
    "DOT",
]

ws = ["SPACE", "TAB", "NEWLINE"]


class IsExpressionStatement(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 25
        self.scope = [Function, ControlStructure]

    def check_reserved_keywords(self, context, pos):
        if context.check_token(pos, keywords) is False:
            return False, pos
        if context.check_token(pos, "RETURN"):
            i = pos + 1
            while context.check_token(i, "SEMI_COLON") is False:
                i += 1
            i += 1
            return True, i
        elif context.check_token(pos, "GOTO"):
            i = pos + 1
            i = context.skip_ws(i)
            while context.check_token(i, ["MULT", "BWISE_AND"]) is True and context.is_operator(i) is False:
                i += 1
            if context.check_token(i, "IDENTIFIER") is False:
                if context.check_token(i, "LPARENTHESIS") is True:
                    # parse label value here
                    i = context.skip_nest(i)
                elif context.debug == 0:
                    raise CParsingError("Error: Goto statement should be followed by a label")
            i += 1
            i = context.skip_ws(i)
            i += 1
            return True, i
        else:
            i = pos + 1
            i = context.skip_ws(i)
            i += 1
            return True, i

    def check_instruction(self, context, pos):
        i = pos
        if context.check_token(i, ["IDENTIFIER"]) is False:
            return False, pos
        i += 1
        # TO DO:
        # Skip possible brackets:
        # eg: "f[0]();" is a valid instruction

        i = context.skip_ws(i)
        if context.check_token(i, "LPARENTHESIS") is False:
            return False, pos

        # Shouldn't use skip_nest, should parse manually ?
        i = context.skip_nest(i)
        i += 1
        i = context.skip_ws(i)
        if context.check_token(i, "SEMI_COLON") is False:
            return False, pos
        i += 1
        return True, i

    def check_inc_dec(self, context, pos):
        i = pos
        ret = False
        if context.check_token(i, ["INC", "DEC"]) is True:
            ret = True
            i += 1
            i = context.skip_ws(i)
        if context.check_token(i, "LPARENTHESIS") is True:
            i = context.skip_nest(i)
            i += 1
            i = context.skip_ws(i)
            if ret is False:
                if context.check_token(i, ["INC", "DEC"]) is False:
                    return False, pos
                i += 1
                i = context.skip_ws(i)
            if context.check_token(i, "SEMI_COLON") is False:
                return False, pos
            i += 1
            return True, i
        if context.check_token(i, "IDENTIFIER") is True:
            i += 1
            if ret is False:
                i = context.skip_ws(i)
                if context.check_token(i, ["INC", "DEC"]) is False:
                    return False, pos
                i += 1
                i = context.skip_ws(i)
            while context.check_token(i, "SEMI_COLON") is False:
                i += 1
            i += 1
            return True, i
        return False, pos

    def void_identifier(self, context, pos):
        if context.check_token(pos, "LPARENTHESIS") is False:
            return False, pos
        i = pos + 1
        if context.check_token(i, "VOID") is False:
            return False, pos
        i += 1
        if context.check_token(i, "RPARENTHESIS") is False:
            return False, pos
        i += 1
        i = context.skip_ws(i)
        if context.check_token(i, "IDENTIFIER") is False:
            return False, pos
        i += 1
        while context.check_token(i, "SEMI_COLON") is False:
            i += 1
        i += 1
        return True, i

    def run(self, context):
        """
        Catches expression statement by elimination
        """
        i = context.skip_ws(0)
        ret, i = self.check_instruction(context, i)
        if ret is False:
            ret, i = self.check_reserved_keywords(context, i)
            #if ret is False:
            #    ret, i = self.check_inc_dec(context, i)
            if ret is False:
                ret, i = self.void_identifier(context, i)
                if ret is False:
                    return False, 0
        i = context.eol(i)
        return True, i
