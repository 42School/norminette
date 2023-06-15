from norminette.lexer import Lexer
from norminette.rules import Rule
from norminette.scope import GlobalScope


class CheckPreprocessorInclude(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsPreprocessorStatement"]

    def run(self, context):
        """
        Includes must be at the start of the file
        You cannot include anything that isn't an header file
        """
        i = 0
        filetype = ""
        if context.check_token(i, "INCLUDE") is False:
            return False, 0
        if (
            type(context.scope) is not GlobalScope
            or context.scope.include_allowed is False
        ):
            context.new_error("INCLUDE_START_FILE", context.peek_token(i))
            return True, i
        val = context.peek_token(i).value.split("include", 1)[1]
        content = Lexer(val, context.peek_token(i).pos[0])
        tkns = content.get_tokens()
        i = 1
        while i < len(tkns) and tkns[i].type in ["TAB", "SPACE"]:
            if tkns[i].type == "TAB":
                context.new_error("TAB_INSTEAD_SPC", tkns[i])
            i += 1
        if i < len(tkns) and tkns[i].type == "LESS_THAN":
            i = len(tkns) - 1
            while i > 0:
                if i < len(tkns) - 1 and tkns[i].type == "DOT":
                    i += 1
                    filetype = tkns[i].value
                    break
                i -= 1
        elif i < len(tkns) and tkns[i].type == "STRING":
            try:
                filetype = tkns[i].value.split(".")[-1][0]
            except:
                filetype = ""
        while tkns[i].type != "NEWLINE" and i < len(tkns) - 1:
            i += 1
        if (tkns[i].type == "NEWLINE" and tkns[i - 1].type in ["SPACE", "TAB"]) or tkns[
            i
        ].type in ["SPACE", "TAB"]:
            context.new_error("SPC_BEFORE_NL", context.peek_token(0))
        if filetype and filetype != "h":
            context.new_error("INCLUDE_HEADER_ONLY", context.peek_token(0))
        return False, 0
