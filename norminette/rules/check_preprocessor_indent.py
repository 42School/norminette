from rules import Rule

ALLOWED_PREPROC = ["DEFINE", "IFNDEF", "IFDEF", "IF", "ELIF", "ELSE", "ENDIF"]
MORE_INDENT = ["DEFINE"]


class CheckPreprocessorIndent(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsPreprocessorStatement"]

    def run(self, context):
        i = 0
        i = context.skip_ws(i)
        tken = context.peek_token(i)
        current_indent = context.preproc_scope_indent
        if context.peek_token(i).pos[1] != 1:
            context.new_error("PREPROC_START_LINE", context.peek_token(0))
        tken = context.peek_token(i)
        if context.check_token(i, ALLOWED_PREPROC) is False:
            context.new_error("PREPROC_UKN_STATEMENT", context.peek_token(i))
        if context.check_token(i, MORE_INDENT) is False:
            current_indent -= 1
        fmt = ''
        val = tken.value[1:] if tken.value else tken.type
        length = 0
        while length < current_indent:
            if val[length] != ' ':
                context.new_error("PREPROC_BAD_INDENT", context.peek_token(i))
            length += 1
        if val[length] == ' ':
            context.new_error("PREPROC_BAD_INDENT", context.peek_token(i))
        context.pop_tokens(1)
        if context.check_token(i, "NEWLINE") is False:
            context.new_error("PREPROC_EXPECTED_EOL", context.peek_token(i))
        return False, 0
