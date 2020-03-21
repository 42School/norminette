from rules import PrimaryRule, Rule
import context
from scope import GlobalScope

pp_keywords = [
                "PRAGMA",
                "INCLUDE",
                "UNDEF",
                "DEFINE",
                "IF",
                "ELIF",
                "ELSE",
                "IFDEF",
                "IFNDEF",
                "ENDIF"]
whitespaces = ["TAB", "SPACE", "NEWLINE"]


class IsPreprocessorStatement(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 10
        self.scope = []

    def run(self, context):
        i = context.skip_ws(0)
        if context.check_token(i, pp_keywords) is True:
            if context.check_token(i, ["IFDEF", "IFNDEF"]):
                context.preproc_scope_indent += 1
            elif context.check_token(i, "ENDIF") \
                    and context.preproc_scope_indent > 0:
                context.preproc_scope_indent -= 1
            i += 1
        else:
            return False, 0
        context.eol(i)
        return True, i
