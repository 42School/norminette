from lexer import Token
from rules import Rule
import string


assigns = [
    'ASSIGN'
]

class CheckIdentifierName(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = []

    def run(self, context):
        """
        Raises 1018 error, bad formated user defined identifier
        """
        i = 0
        legal_characters = string.ascii_lowercase + string.digits + '_'
        legal_cap_characters = string.ascii_uppercase + string.digits + '_'
        if context.history[-1] == "IsFuncDeclaration" or context.history[-1] == "IsFuncPrototype":
            for c in context.scope.fnames[-1]:
                if c not in legal_characters:
                    context.new_error(
                                    "FORBIDDEN_CHAR_NAME",
                                    context.peek_token(context.fname_pos))
                    break
        passed_assign = False
        err = None
        hist = context.history[-1]
        while i < context.tkn_scope and context.peek_token(i) is not None:
            if context.check_token(i, assigns) is True:
                passed_assign = True
            if context.check_token(i, "IDENTIFIER"):
                for c in context.peek_token(i).value:
                    if c not in legal_characters:
                        err = ("FORBIDDEN_CHAR_NAME", context.peek_token(i))
                        break
                if err is not None and hist not in ['IsFuncDeclaration', 'IsFuncPrototype'] or (hist == 'IsVariable' and passed_assign == True):
                    for c in context.peek_token(i).value:
                        if c not in legal_cap_characters:
                            err = ("FORBIDDEN_CHAR_NAME", context.peek_token(i))
                            break
                    else:
                        err = None
                if err is not None:
                    context.new_error(err[0], err[1])
            i += 1
            #elif context.peek_token(i) == "DEFINE":
                #content = Lexer(context.peek_token(i).value)
                #tkns = content.get_tokens()
                #v = 0
                #while v < len(tkns):
                    #if tkns[v] == "IDENTIFIER":
                        #for c in tkns[v].value:
                            #if c not in legal_characters:
                                #context.new_error(
                                                #"FORBIDDEN_CHAR_NAME",
                                                #context.peek_token(tkns[v]))
                                #break
        return False, 0
