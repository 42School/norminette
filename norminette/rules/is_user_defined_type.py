from lexer import Token
from rules import PrimaryRule
from context import GlobalScope, UserDefinedType
from exceptions import CParsingError

utypes = ["TYPEDEF", "UNION", "STRUCT", "ENUM"]


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
            return False, pos
        ret, i = context.check_identifier(i)
        print (ret, i)
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
        i = context.skip_ws(0, nl=False)
        while context.check_token(i, utypes) is False:
            if context.peek_token(i) is None:
                return False, 0
            if context.check_token(i, ['NEWLINE', 'SEMI_COLON']) is True:
                return False, 0
            i += 1
        while context.check_token(i, ["NEWLINE", "SEMI_COLON"]) is False:
            i += 1
        if context.check_token(i, "NEWLINE") is True:
            context.sub = context.scope.inner(UserDefinedType)
            i = context.eol(i)
            return True, i
        elif context.check_token(i, "SEMI_COLON") is True:
            i += 1
            i = context.eol(i)
            return True, i

        #i = context.skip_ws(0)
        #ret, i = context.check_type_specifier(i, True)
        #print (ret, i, context.peek_token(i))
        #if ret is False:
            #return False, 0
        #ret, i = self.typedef(context, i)
        #if ret is True:
            #i = context.skip_ws(i, nl=False)
            #print (context.peek_token(i))
            #if context.check_token(i, "SEMI_COLON") is True:
                #i = context.eol(i)
                #return True, i
#
            #elif context.check_token(i, "NEWLINE") is True:
                #i += 1
                #i = context.eol(i)
                #context.sub = context.scope.inner(UserDefinedType)
                #if "TYPEDEF" in [tkn.type for tkn in context.tokens[:i]]:
                    #context.sub.typedef = True
            #elif context.check_token(i, "SEMI_COLON") is True:
                #i += 1
            #else:
                #return False, 0
            #i = context.eol(i)
            #return True, i
        #ret, i = self.utype_definition(context, i)
        #if ret is True:
            #i = context.skip_ws(i)
            #if context.check_token(i, "LBRACE") is True:
                #i += 1
                #i = context.eol(i)
                #context.sub = context.scope.inner(UserDefinedType)
            #elif context.check_token(i, "SEMI_COLON") is True:
                #i += 1
            #else:
                #return False, 0
            #i = context.eol(i)
            #return True, i
        #return False, 0
