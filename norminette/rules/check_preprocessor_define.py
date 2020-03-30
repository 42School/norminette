from rules import Rule
from lexer import Lexer, TokenError


class CheckPreprocessorDefine(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsPreprocessorStatement"]

    def run(self, context):
        i = 0
        print("checkpreprocdefine", context.tokens[:3])
        if context.check_token(i, "DEFINE") is False:
            return False, 0
        val = context.peek_token(i).value.split("define")[1]
        content = Lexer(val)
        tkns = content.get_tokens()
        while context.check_token(i, ["TAB", "SPACE"]) is True:
            i += 1
        i += 1
        if tkns[i].type != "IDENTIFIER":
            context.new_error("PREPROC_CONSTANT", context.peek_token(0))
        i += 1
        while context.check_token(i, ["TAB", "SPACE"]) is True:
            i += 1
        i += 1
        if context.check_token(i, ["CONSTANT", "STRING", "STRUCT"]):
            context.new_error("PREPROC_CONSTANT", context.peek_token(0))
        i += 1
        return False, 0
