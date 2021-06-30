from norminette.lexer import Lexer
from norminette.rules import Rule
from norminette.scope import GlobalScope, Function


class CheckPreprocessorDefine(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsPreprocessorStatement"]

    def skip_define_nest(self, i, tkns):
        eq = {
            "LPARENTHESIS": "RPARENTHESIS",
            "LBRACKET": "RBRACKET",
            "LBRACE": "RBRACE",
        }
        eq_val = eq[tkns[i].type]
        while i < len(tkns) and tkns[i].type != eq_val:
            i += 1
        return i

    def check_function_declaration(self, context):
        i = context.skip_ws(0)
        if context.check_token(i, ["#IF", "#ELSE", "IFDEF", "IFNDEF"]) is False:
            return
        context.tmp_scope = context.scope
        context.scope = context.scope.get_outer()

    def run(self, context):
        """
        Preprocessor statements must be defined only in the global scope
        Defined names must be in capital letters
        Define cannot contain newlines
        Define can only contain constant values, such as integers and strings
        """
        i = context.skip_ws(0)
        if len(context.history) > 1 and context.history[-2] == "IsFuncDeclaration":
            self.check_function_declaration(context)
        if type(context.scope) is not GlobalScope:
            if type(context.scope) == Function and context.scope.multiline == False:
                pass
            else:
                context.new_error("PREPROC_GLOBAL", context.peek_token(0))
        if context.check_token(i, "DEFINE") is False:
            return False, 0
        val = context.peek_token(i).value.split("define", 1)[1]
        content = Lexer(val, context.peek_token(i).pos[0])
        tkns = content.get_tokens()
        i = 0
        identifiers = []
        protection = context.filename.upper().split("/")[-1].replace(".", "_")
        for tkn in tkns:
            if tkn.type == "ESCAPED_NEWLINE":
                context.new_error("NEWLINE_DEFINE", tkn)
            elif tkn.type in ["TAB", "SPACE"]:
                i += 1
                continue
            elif tkn.type == "IDENTIFIER" and len(identifiers) == 0:
                if tkn.value.isupper() is False:
                    context.new_error("MACRO_NAME_CAPITAL", tkn)
                identifiers.append(tkn)
                tmp = i
                while tmp < len(tkns) - 1 and tkns[tmp].type in [
                    "SPACE",
                    "TAB",
                    "IDENTIFIER",
                ]:
                    tmp += 1
                if tmp == (len(tkns) - 1) and context.filetype == "h":
                    if context.scope.header_protection == 0:
                        if identifiers[0].value == protection:
                            context.scope.header_protection = 1
                        elif identifiers[0].value != protection:
                            context.new_error("HEADER_PROT_NAME", tkns[1])
                elif (
                    context.filetype == "c"
                    and context.scope.include_allowed == True
                    and (
                        len(tkns) > tmp + 1
                        or (
                            len(tkns) == tmp + 1
                            and identifiers[0].value != protection
                            and context.scope.header_protection == -1
                        )
                    )
                ):
                    context.scope.include_allowed = False

            elif tkn.type in ["IDENTIFIER", "STRING", "CONSTANT"]:
                if context.skip_define_error == True:
                    continue
                if len(identifiers) == 1:
                    if tkn.type == "IDENTIFIER" and tkn.value.isupper() is False:
                        context.new_error("PREPROC_CONSTANT", tkn)
                    identifiers.append(tkn)
                elif len(identifiers) == 0:
                    context.new_error("INCORRECT_DEFINE", tkn)
                else:
                    context.new_error("TOO_MANY_VALS", tkn)
            elif tkn.type == "LPARENTHESIS":
                if context.skip_define_error == True:
                    continue
                if len(identifiers) == 0:
                    continue
                elif len(identifiers) == 1 and tkns[i - 1].type in ["SPACE", "TAB"]:
                    continue
                else:
                    context.new_error("PREPROC_CONSTANT", tkn)
            elif tkn.type in ["LBRACKET", "LBRACE"]:
                if context.skip_define_error == True:
                    continue
                context.new_error("PREPROC_CONSTANT", tkn)

            i += 1
        if context.filetype == "h" and context.scope.header_protection != 1:
            context.new_error("HEADER_PROT_ALL", context.peek_token(0))
        return False, 0
