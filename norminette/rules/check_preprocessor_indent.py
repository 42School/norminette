from norminette.rules import Rule

ALLOWED_PREPROC = [
    "DEFINE",
    "IFNDEF",
    "IFDEF",
    "#IF",
    "ELIF",
    "#ELSE",
    "ENDIF",
    "INCLUDE",
    "WARNING",
    "UNDEF",
    "ERROR"
]
TOO_MUCH_INDENT = ["IFNDEF", "IFDEF", "ELIF", "#IF", "#ELSE"]


class CheckPreprocessorIndent(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsPreprocessorStatement"]

    def get_space_number(self, val):
        val = val[1:]
        spaces = 0
        for i in val:
            if i == " ":
                spaces += 1
            else:
                return spaces

    def run(self, context):
        """
        Preprocessor statements must be indented by an additionnal space for each #ifdef/#ifndef/#if
        statement.
        Structure is `#{indentation}preproc_statement`
        Preprocessor must always be at the start of the line
        """
        i = 0
        i = context.skip_ws(i)
        tken = context.peek_token(i)
        current_indent = context.preproc_scope_indent
        if context.peek_token(i).pos[1] != 1:
            context.new_error("PREPROC_START_LINE", context.peek_token(0))
        tken = context.peek_token(i)
        if context.check_token(i, ALLOWED_PREPROC) is False:
            context.new_error("PREPROC_UKN_STATEMENT", context.peek_token(i))
        if context.check_token(i, TOO_MUCH_INDENT) is True:
            current_indent -= 1
        if current_indent < 0:
            current_indent = 0
        fmt = ""
        val = tken.value[1:] if tken.value else tken.type
        spaces = self.get_space_number(tken.value if tken.value else tken.type)
        if current_indent != spaces:
            context.new_error("PREPROC_BAD_INDENT", context.peek_token(i))

        i += 1
        tken = context.peek_token(i)
        if tken is not None and tken.type not in ["NEWLINE", "COMMENT", "MULT_COMMENT"]:
            context.new_error("PREPROC_EXPECTED_EOL", context.peek_token(i))
        return False, 0
