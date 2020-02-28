from lexer import Token
from rules import PrimaryRule


utypes = ["UNION", "STRUCT", "ENUM"]

class CheckUdefType(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 10

    def utype_definition(self, context, pos):
        i = pos
        i = self.skip_ws(context, i)
        if context.check_token(i, utypes) is False:
            return False, pos
        ret, i = self.check_type_specifier(context, i)
        if ret is False:
            return False, pos
        i += 1
        i = self.skip_ws(context, i)
#        i = 1
        if context.check_token(i, "SEMI_COLON") is True:
            i += 1
            return True, i
        if context.check_token(i, "LBRACE") is True:
            i += 1
            i = self.skip_nest(context, i, "RBRACE")
            i += 1
            i = self.skip_ws(context, i)
            if context.check_token(i, "SEMI_COLON") is False:
                # Coming this far an not encountering a SEMI_COLON is 
                # a fatal error
                return False, pos
            i += 1
            return True, i
        return False, pos

    def typedef(self, context, pos):
        i = pos
        if context.check_token(i, "TYPEDEF") is False:
            return False, pos

        i += 1
        ret, i = self.check_type_specifier(context, i)
        if ret is False:
            # most likely a "fatal" error since typedef keyword was found
            return False, pos
        i += 1
        if [utype for utype in context.tokens[:i] if utype.type in utypes]:
            i = self.skip_ws(context, i)
            if context.check_token(i, "IDENTIFIER") is True:
                i += 1
                i = self.skip_ws(context, i)
                if context.check_token(i, "SEMI_COLON") is False:
                    # most likely a "fatal" error since typedef
                    # keyword was found
                    return False, pos
                i += 1
                return True, i
            if context.check_token(i, "RBRACE") is True:
                i = self.skip_brace(context, i)
                i += 1
                i = self.skip_ws(context, i)
                if context.check_token(i, "IDENTIFIER") is False:
                    return False, 0
                i += 1
                i = self.skip_ws(context, i)
                if context.check_token(i, "SEMI_COLON") is False:
                    return False, 0
                return True, i
            # most likely a "fatal" error since typedef keyword was found
            return False, pos
        i = self.skip_ws(context, i)
        if context.check_token(i, "IDENTIFIER") is False:
            return False, pos
        i += 1
        i = self.skip_ws(context, i)
        if context.check_token(i, "SEMI_COLON") is False:
            return False, 0
        i += 1
        return True, i

    def run(self, context):
        i = self.skip_ws(context, 0)
        ret, i = self.typedef(context, i)
        if ret is True:
            return True, i
        ret, i = self.utype_definition(context, i)
        if ret is True:
            return True, i
        return False, 0
