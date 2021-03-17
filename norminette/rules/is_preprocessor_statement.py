from norminette.rules import PrimaryRule

pp_keywords = [
    "PRAGMA",
    "INCLUDE",
    "UNDEF",
    "DEFINE",
    "#IF",
    "ELIF",
    "#ELSE",
    "IFDEF",
    "IFNDEF",
    "ENDIF",
    "ERROR",
    "WARNING",
    "IMPORT",
]

whitespaces = ["TAB", "SPACE", "NEWLINE"]


class IsPreprocessorStatement(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 85
        self.scope = []

    def run(self, context):
        """
        Catches any kind of preprocessor statements
        Handles indentation related informations
        """
        i = context.skip_ws(0)
        if context.check_token(i, pp_keywords) is True:
            if context.peek_token(i).value is None or context.peek_token(i).value.startswith("#") is False:
                return False, 0
            if context.check_token(i, ["IFDEF", "IFNDEF", "#IF", "#ELIF"]):
                context.preproc_scope_indent += 1
            elif context.check_token(i, "ENDIF") and context.preproc_scope_indent > 0:
                context.preproc_scope_indent -= 1
            i += 1
        else:
            return False, 0
        i = context.eol(i)
        return True, i
