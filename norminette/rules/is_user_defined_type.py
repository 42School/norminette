from lexer import Token
from rules import PrimaryRule
from context import GlobalScope, UserDefinedType


utypes = ["UNION", "STRUCT", "ENUM"]


class IsUserDefinedType(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 10
        self.scope = [GlobalScope, UserDefinedType]

    def utype_definition(self, context, pos):
        i = pos
        if context.check_token(i, utypes) is False:
            return False, pos
        i += 1
        i = context.skip_ws(i)
        if context.check_token(i, "IDENTIFIER") is False:
            if type(context.scope) is not UserDefinedType:
                return False, 0
            i = context.skip_ws(i)
            if context.check_token(i, "LBRACE") is False:
                return False, pos
            context.sub = context.scope.inner(UserDefinedType)
            # print(context.tokens[i])
            i += 1
            return True, i
        i += 1
        i = context.skip_ws(i)
        if context.check_token(i, "SEMI_COLON") is True:
            i += 1
            return True, i
        if context.check_token(i, "LBRACE") is True:
            i += 1
            context.sub = context.scope.inner(UserDefinedType)
            i = context.skip_nest(i)
            return True, i
        return False, pos

    def typedef(self, context, pos):
        i = pos
        if context.check_token(i, "TYPEDEF") is False:
            return False, pos

        i += 1
        ret, i = context.check_type_specifier(i)
        if ret is False:
            # most likely a "fatal" error since typedef keyword was found
            return False, pos
        if [utype for utype in context.tokens[:i] if utype.type in utypes]:
            i += 1
            i = context.skip_ws(i)
            # print(context.tokens[:i], context.peek_token(i))
            if context.check_token(i, "IDENTIFIER") is True:
                i += 1
                i = context.skip_ws(i)
                if context.check_token(i, "SEMI_COLON") is False:
                    # most likely a "fatal" error since typedef
                    # keyword was found
                    return False, pos
                i += 1
                return True, i
            if context.check_token(i, "LBRACE") is True:
                i += 1
                context.sub = context.scope.inner(UserDefinedType)
                context.sub.typedef = True
                return True, i
            # most likely a "fatal" error since typedef keyword was found
            return False, pos
        i = context.skip_ws(i)
        if context.check_token(i, "IDENTIFIER") is False:
            return False, pos
        i += 1
        i = context.skip_ws(i)
        if context.check_token(i, "SEMI_COLON") is False:
            return False, pos
        i += 1
        return True, i

    def run(self, context):
        i = context.skip_ws(0)
        ret, i = self.typedef(context, i)
        if ret is True:
            i = context.eol(i)
            return True, i
#        print(ret, i, context.peek_token(i))
        ret, i = self.utype_definition(context, i)
        if ret is True:
            i = context.eol(i)
            return True, i
        return False, 0
