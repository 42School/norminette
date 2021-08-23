import string

from norminette.rules import Rule
from norminette.scope import GlobalScope, UserDefinedType


assigns = ["ASSIGN"]


class CheckIdentifierName(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = []

    def run(self, context):
        """
        Function can only be declared in the global scope
        User defined identifiers can only contain lowercase characters, '_' or digits
        """
        i = 0
        legal_characters = string.ascii_lowercase + string.digits + "_"
        legal_cap_characters = string.ascii_uppercase + string.digits + "_"
        if context.history[-1] == "IsFuncDeclaration":
            sc = context.scope
            if type(sc) is not GlobalScope and type(sc) is not UserDefinedType:
                context.new_error("WRONG_SCOPE_FCT", context.peek_token(0))
            while type(sc) != GlobalScope:
                sc = sc.outer()
            for c in sc.fnames[-1]:
                if c not in legal_characters:
                    context.new_error("FORBIDDEN_CHAR_NAME", context.peek_token(context.fname_pos))
        if len(context.scope.vars_name) > 0:
            for val in context.scope.vars_name[::]:
                for c in val.value:
                    if c not in legal_characters:
                        context.new_error("FORBIDDEN_CHAR_NAME", val)
                        break
                context.scope.vars_name.remove(val)
        # passed_assign = False
        # err = None
        # hist = context.history[-1]
        # while i < context.tkn_scope and context.peek_token(i) is not None:
        # if context.check_token(i, assigns) is True:
        # passed_assign = True
        #        if context.check_token(i, "IDENTIFIER") and hist in ['IsVarDeclaration']:
        # for c in context.peek_token(i).value:
        # if c not in legal_characters:
        # err = ("FORBIDDEN_CHAR_NAME", context.peek_token(i))
        # break
        # if err is not None and hist not in ['IsFuncDeclaration', 'IsFuncPrototype'] or (hist == 'IsVariable' and passed_assign == True):
        # for c in context.peek_token(i).value:
        # if c not in legal_cap_characters:
        # err = ("FORBIDDEN_CHAR_NAME", context.peek_token(i))
        # break
        # else:
        # err = None
        # if err is not None:
        # context.new_error(err[0], err[1])
        # break
        # i += 1
        return False, 0
