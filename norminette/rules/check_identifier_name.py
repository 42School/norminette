from lexer import Token
from rules import Rule
import string


class CheckIdentifierName(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = []

    def run(self, context):
        """
        Raises 1018 error, bad formated user defined identifier
        """
        legal_characters = string.ascii_lowercase + string.digits + '_' + '&*'
        if context.history[-1] == "IsFuncDeclaration" or context.history[-1] == "IsFuncPrototype":
            for c in context.scope.fnames[-1]:
                if c not in legal_characters:
                    context.new_error(
                                    "FORBIDDEN_CHAR_NAME",
                                    context.peek_token(context.fname_pos))
                    break
        else:
            _, i = context.check_type_specifier(0)
            while context.peek_token(i) is not None and context.check_token(i, ["IDENTIFIER", "NEWLINE"]) is False:
                i += 1
            if context.peek_token(i) == "IDENTIFIER":
                for c in context.peek_token(i).value:
                    if c not in legal_characters:
                        context.new_error(
                                        "FORBIDDEN_CHAR_NAME",
                                        context.peek_token(context.fname_pos))
                        break
            #elif context.peek_token(i) == "DEFINE":
                #content = Lexer(context.peek_token(i).value)
                #tkns = content.get_tokens()
                #v = 0
                #while v < len(tkns):
                    #print (tkns[v])
                    #if tkns[v] == "IDENTIFIER":
                        #for c in tkns[v].value:
                            #if c not in legal_characters:
                                #context.new_error(
                                                #"FORBIDDEN_CHAR_NAME",
                                                #context.peek_token(tkns[v]))
                                #break
        return False, 0
