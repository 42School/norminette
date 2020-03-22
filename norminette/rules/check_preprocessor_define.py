from rules import Rule
from lexer import Lexer, TokenError


class CheckPreprocessorDefine(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsPreprocessorStatement"]

    def run(self, context):
        i = 0
        if context.check_token(i, "DEFINE") is False:
            return False, 0
        val = context.peek_token(i).value.split("define")[1]
        content = Lexer(val)
        tkns = content.get_tokens()
        while tkns[i].type in ["TAB", "SPACE"]:
            i += 1
        if tkns[i].type != "IDENTIFIER":
            context.new_error("PREPROC_CONSTANT", context.peek_token(0))
        i += 1
        while tkns[i].type in ["TAB", "SPACE"]:
            i += 1
        if tkns[i].type not in ["CONSTANT", "STRING", "STRUCT"]:
            context.new_error("PREPROC_CONSTANT", context.peek_token(0))
        i += 1
        return False, 0
