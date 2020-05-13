from rules import Rule
from lexer import Lexer, TokenError
from scope import *


class CheckPreprocessorInclude(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsPreprocessorStatement"]

    def run(self, context):
        i = 0
        if context.check_token(i, "INCLUDE") is False:
            return False, 0
        if type(context.scope) is not GlobalScope or context.scope.include_allowed == False:
            context.new_error("INCLUDE_START_FILE", context.peek_token(i))
            return True, i
        val = context.peek_token(i).value.split("include")[1]
        content = Lexer(val)
        tkns = content.get_tokens()
        i = 1
        while context.check_token(i, ["TAB", "SPACE"]):
            i += 1
        if tkns[i].type == "LESS_THAN":
            while tkns[i].type != "DOT":
                i += 1
            i += 1
            filetype = tkns[i].value
        elif tkns[i].type == "STRING":
            try:
                filetype = tkns[i].value.split('.')[-1][0]
            except:
                filetype = ''
        if filetype == 'c':
            context.new_error("INCLUDE_HEADER_ONLY", context.peek_token(0))
        return False, 0
