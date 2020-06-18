from lexer import Token
from rules import PrimaryRule
from context import GlobalScope, UserDefinedType
from exceptions import CParsingError
from scope import *

utypes = ["TYPEDEF", "UNION", "STRUCT", "ENUM"]


class IsUserDefinedType(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 12
        self.scope = [GlobalScope, UserDefinedType]


    def typedef(self, context, pos):
        i = context.skip_ws(pos)
        if "TYPEDEF" not in [tkn.type for tkn in context.tokens[:i]]:
            return False, pos
        ret, i = context.check_identifier(i)
        if ret is False:
            i += 1
            if context.check_token(i, "LBRACE"):
                return True, i
            return False, pos
        i += 1
        return True, i

    def utype_definition(self, context, pos):
        utypes = ["STRUCT", "ENUM", "UNION"]
        if not [tkn for tkn in context.tokens[:pos] if tkn.type in utypes]:
            return False, pos
        return True, pos
        i = context.skip_ws(i)
        return ret, i

    def run(self, context):
        """
            Catches user type definitions
            Can include the whole type definition in case it's a structure
            Variable declarations aren't included
        """
        i = context.skip_ws(0, nl=False)
        enum = False
        while context.check_token(i, utypes) is False:
            if context.peek_token(i) is None:
                return False, 0
            if context.check_token(i, ['NEWLINE', 'SEMI_COLON']) is True:
                return False, 0
            i += 1
        while context.check_token(i, ["NEWLINE", "SEMI_COLON"]) is False:
            if context.check_token(i, "ENUM") is True:
                enum = True
            i += 1
        if context.check_token(i, "NEWLINE") is True:
            if enum == True:
                context.sub = context.scope.inner(UserDefinedEnum)
            else:
                context.sub = context.scope.inner(UserDefinedType)
            i = context.eol(i)
            return True, i
        elif context.check_token(i, "SEMI_COLON") is True:
            i += 1
            i = context.eol(i)
            return True, i
