from norminette.rules import Rule


class CheckPreprocessorIndent(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsPreprocessorStatement"]

    def run(self, context):
        """
        Preprocessor statements must be indented by an additionnal space for each #ifdef/#ifndef/#if
        statement.
        Structure is `#{indentation}preproc_statement`
        Preprocessor must always be at the start of the line
        """
        i = context.skip_ws(0)

        hash_ = context.peek_token(i)
        if hash_ and hash_.line_column != 1:
            context.new_error("PREPROC_START_LINE", hash_)
        i += 1
        n = context.skip_ws(i)
        while context.check_token(i, "SPACE"):
            i += 1
        if context.check_token(i, "TAB"):
            context.new_error("TAB_REPLACE_SPACE", context.peek_token(i))
        i = n

        spaces = context.peek_token(i).line_column - hash_.line_column - 1
        indent = context.preproc_scope_indent
        if context.check_token(i, ("IF", "ELSE")):
            indent -= 1
            i += 1
        else:
            t = context.peek_token(i)
            if t and t.type == "IDENTIFIER" and t.value.upper() in ("IFNDEF", "IFDEF", "ELIF"):
                indent -= 1
                i += 1

        if spaces > indent:
            context.new_error("TOO_MANY_WS", hash_)
        if spaces < indent:
            context.new_error("PREPROC_BAD_INDENT", hash_)
