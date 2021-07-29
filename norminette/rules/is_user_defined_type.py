from norminette.rules import PrimaryRule
from norminette.scope import UserDefinedType, GlobalScope, UserDefinedEnum
import pdb

utypes = ["TYPEDEF", "UNION", "STRUCT", "ENUM"]


class IsUserDefinedType(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 45
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
        p = 0
        ids = []
        while context.peek_token(i) is not None:
            if context.check_token(i, utypes) is True and p <= 0:
                break
            if context.check_token(i, "LPARENTHESIS") is True:
                p += 1
            if context.check_token(i, "RPARENTHESIS") is True:
                p -= 1
            if context.check_token(i, ["NEWLINE", "SEMI_COLON"]) is True:
                return False, 0
            i += 1
        if context.peek_token(i) is None:
            return False, 0
        p = 0
        while context.peek_token(i):
            if context.check_token(i, "LPARENTHESIS") is True:
                p += 1
            if context.check_token(i, "RPARENTHESIS") is True:
                p -= 1
            if context.check_token(i, "ENUM") is True:
                enum = True
            if context.check_token(i, ["NEWLINE", "SEMI_COLON"]) is True and p == 0:
                break
            if context.check_token(i, "IDENTIFIER"):
                ids.append(context.peek_token(i))
            i += 1
        if context.check_token(i, "NEWLINE") is True and p <= 0:
            if enum == True:
                context.sub = context.scope.inner(UserDefinedEnum)
            else:
                context.sub = context.scope.inner(UserDefinedType)
            i = context.eol(i)
            return True, i
        elif context.check_token(i, "SEMI_COLON") is True:
            i += 1
            context.scope.vars_name.append(ids[-1])
            i = context.eol(i)
            return True, i
