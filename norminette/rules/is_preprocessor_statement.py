from rules import PrimaryRule, Rule
import context
from scope import GlobalScope


ps_keywords = ["DEFINE"]
pm_keywords = ["IF", "ELIF", "ELSE"]
pcs_keywords = ["IFDEF", "IFNDEF"]
pcs_end = ["ENDIF"]
whitespaces = ["TAB", "SPACE", "NEWLINE"]



class IsPreprocessorStatement(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 10
        self.scope = []

    def run(self, context):
        i = context.skip_ws(0)
        if context.check_token(i, pcs_keywords) is True:
            i += 1
            context.preproc_scope_indent += 1
        elif context.check_token(i, pcs_end) is True:
            i += 1
            context.preproc_scope_indent -= 1 if context.preproc_scope_indent > 0 else 0
        elif context.check_token(i, pm_keywords + ps_keywords) is True:
            i += 1
            context.eol(i)
            return True, i
        else:
            return False, 0
        context.eol(i)
        return True, i