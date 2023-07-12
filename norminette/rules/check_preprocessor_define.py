from norminette.rules import Rule


class CheckPreprocessorDefine(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsPreprocessorStatement"]

    def run(self, context):
        """
        Defined names must be in capital letters
        Define can only contain constant values, such as integers and strings
        """
        i = context.skip_ws(0)
        i += 1  # skip HASH
        i = context.skip_ws(i)
        if not context.check_token(i, "IDENTIFIER"):
            return
        if not context.peek_token(i).value == "define":
            return
        if context.preproc.skip_define:
            return
        i += 1  # skip DEFINE
        i = context.skip_ws(i)

        if not context.peek_token(i).value.isupper():
            context.new_error("MACRO_NAME_CAPITAL", context.peek_token(i))
        i += 1  # skip macro name

        if context.check_token(i, "LPARENTHESIS"):
            context.new_error("MACRO_FUNC_FORBIDDEN", context.peek_token(i))
            while not context.check_token(i, "RPARENTHESIS"):
                i += 1
            i += 1
        i = context.skip_ws(i)

        # It is obscure what `#define` can hold in its value, see:
        # - https://github.com/42School/norminette/issues/12
        # - https://github.com/42School/norminette/issues/127
        # - https://github.com/42School/norminette/issues/282
        #
        if context.check_token(i, ("MINUS", "PLUS", "BWISE_NOT")):
            i += 1
            i = context.skip_ws(i)
            if not context.check_token(i, ("CONSTANT", "IDENTIFIER")):
                context.new_error("PREPROC_CONSTANT", context.peek_token(i))
                return
            i += 1
        elif context.check_token(i, ("CONSTANT", "IDENTIFIER", "STRING")):
            i += 1

        i = context.skip_ws(i, comment=True)
        if context.peek_token(i) and not context.check_token(i, "NEWLINE"):
            context.new_error("PREPROC_CONSTANT", context.peek_token(i))
