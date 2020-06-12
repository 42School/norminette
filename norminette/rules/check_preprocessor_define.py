from rules import Rule
from lexer import Lexer, TokenError
from scope import *


class CheckPreprocessorDefine(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsPreprocessorStatement"]

    def skip_define_nest(self, i, tkns):
        eq = {
            'LPARENTHESIS': 'RPARENTHESIS',
            'LBRACKET': 'RBRACKET',
            'LBRACE': 'RBRACE'
        }
        eq_val = eq[tkns[i].type]
        while i < len(tkns) and tkns[i].type != eq_val:
            i += 1
        return i

    def check_function_declaration(self, context):
        i = context.skip_ws(0)
        if context.check_token(i, ['#IF', "#ELSE", "IFDEF", "IFNDEF"]) is False:
            return
        context.tmp_scope = context.scope
        context.scope = context.scope.get_outer()

    def run(self, context):
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
        val = context.peek_token(i).value.split("define")[1]
        content = Lexer(val, context.peek_token(i).pos[0])
        tkns = content.get_tokens()
        i = 1
        for tkn in tkns:
            if tkn.type == "ESCAPED_NEWLINE":
                context.new_error("NEWLINE_DEFINE", tkn)
        while tkns[i] in ["TAB", "SPACE"]:
            i += 1
        if tkns[i].type == "IDENTIFIER" and tkns[i].value.isupper() is False:
            context.new_error("MACRO_NAME_CAPITAL", context.peek_token(0))
        protection = context.filename.upper().split('/')[-1].replace('.', '_')
        if len(tkns) == i + 1 and context.filetype == 'h':
            if context.scope.header_protection == 0:
                if tkns[1].value == protection:
                    context.scope.header_protection = 1
                elif tkns[1].value != protection:
                    context.new_error("HEADER_PROT_NAME", context.peek_token(i))
        elif context.filetype == 'h' and context.scope.include_allowed == True and \
            (len(tkns) > i + 1 or (len(tkns) == i + 1 and tkns[1].value != protection \
            and context.scope.header_protection == -1 )):
                context.scope.include_allowed = False
        i += 1
        if context.filetype == 'h' and context.scope.header_protection != 1:
            context.new_error("HEADER_PROT_ALL", context.peek_token(0))
        if len(tkns) > i and tkns[i].type not in ['TAB', "SPACE"]:
            if tkns[i].type in ["LPARENTHESIS", "LBRACKET", "RPARENTHESIS"]:
                i = self.skip_define_nest(i, tkns)
            context.new_error("PREPROC_CONSTANT", context.peek_token(0))
            while len(tkns) > i and tkns[i].type not in ['TAB', "SPACE"]:
                i += 1
        while len(tkns) > i and tkns[i].type in ["TAB", "SPACE"]:
            i += 1
        if len(tkns) > i and tkns[i].type == "IDENTIFIER" and tkns[i].value.isupper() is False:
            context.new_error("PREPROC_CONSTANT", context.peek_token(0))
        elif len(tkns) > i and tkns[i].type not in ["STRING", "CONSTANT"]:
            context.new_error("PREPROC_CONSTANT", context.peek_token(0))
        i += 1
        while len(tkns) > i and tkns[i].type in ['SPACE', 'TAB']:
            i += 1
        if len(tkns) > i and tkns[i].type != 'NEWLINE':
            context.new_error("TOO_MANY_VALS", context.peek_token(0))
        return False, 0
