from lexer import Token
from rules import PrimaryRule
from context import GlobalScope, UserDefinedType
from exceptions import CParsingError

utypes = ["UNION", "STRUCT", "ENUM"]


class IsUserDefinedType(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 10
        self.scope = [GlobalScope, UserDefinedType]

    """
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
        ret, i = context.check_type_specifier(i, True)
        if ret is False :
            return False, pos

        if [utype for utype in context.tokens[:i] if utype.type in utypes]:
            i += 1
            i = context.skip_ws(i)
            if context.check_token(i, "IDENTIFIER") is True:
                i += 1
                i = context.skip_ws(i)
                if context.check_token(i, "SEMI_COLON") is False:
                    # most likely a "fatal" error since typedef
                    # keyword was found
                    print(context.tokens[:i], context.tokens[i], context.filename)
                    raise CParsingError("No semi colon found after typedef")
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
    """

    def typedef(self, context, pos):
        i = context.skip_ws(pos)
        if "TYPEDEF" not in [tkn.type for tkn in context.tokens[:i]]:
            return False, 0
        ret, i = context.check_identifier(i)
        print("in typedef after checking IDENTIFIER -->", ret, context.tokens[:i])
        if ret is False:
            if context.check_token(i, "LBRACE"):
                return True, i
            return False, 0
        i += 1
        return True, i

    def utype_definition(self, context, pos):
        utypes = ["STRUCT", "ENUM", "UNION"]
        if not [tkn for tkn in context.tokens[:pos] if tkn.type in utypes]:
            return False, 0
        ret, i = context.check_identifier(pos)
        print("in utype_definition after checking IDENTIFIER -->", ret)
        if ret is False:
            i = context.skip_ws(i)
            return False, 0
        pass

    def run(self, context):
        i = context.skip_ws(0)
        if context.check_token(i, "RBRACE"):
            # Closing udef_type_scope
            i += 1
            ret, i = context.check_type_specifier(i, True)
            ret, i = self.typedef(context, i)
            print("RBRACE", ret)
            return ret, i
        ret, i = context.check_type_specifier(i, True)
        if ret is False:
            return False, 0
        ret, i = self.typedef(context, i)
        if ret is True:
            i = context.skip_ws(i)
            if context.check_token(i, "LBRACE") is True:
                i += 1
                i = context.eol(i)
                context.sub = context.scope.inner(UserDefinedType)
            elif context.check_token(i, "SEMI_COLON") is True:
                i += 1
            else:
                raise CParsingError("Unexpected token after user type \
declaration")
            i = context.eol(i)
            return True, i
        ret, i = self.utype_definition(context, i)
        if ret is True:
            i = context.eol(i)
            return True, i
        return False, 0
