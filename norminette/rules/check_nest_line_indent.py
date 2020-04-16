from rules import Rule
from scope import *


nest_kw = ["RPARENTHESIS", "LPARENTHESIS", "NEWLINE"]

class CheckNestLineIndent(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsControlStatement"]

    def find_nest_content(self, context, nest, i):
        indent = 0
        expected = context.scope.indent + nest
        while context.check_token(i, nest_kw) is False:
            i += 1
        if context.check_token(i, "NEWLINE") is True:
            if context.check_token(i - 1, ["OR", "AND"]):
                context.new_error("EOL_OPERATOR", context.peek_token(i - 1))
            i += 1
            while context.check_token(i, "TAB") is True:
                indent += 1
                i += 1
            if indent > expected:
                context.new_error("TOO_MANY_TAB", context.peek_token(i))
            elif indent < expected:
                context.new_error("TOO_FEW_TAB", context.peek_token(i))
        elif context.check_token(i, "LPARENTHESIS") is True:
            nest += 1
            return self.find_nest_content(context, nest, i)
        elif context.check_token(i, "RPARENTHESIS"):
            return False, 0
        return False, 0

    def run(self, context):
        i = 0
        expected = context.scope.indent
        nest = 0
        if context.history[-1] == "IsEmptyLine":
            return False, 0
        while context.check_token(i, ["LPARENTHESIS", "NEWLINE"]) is False:
            i += 1
        if context.check_token(i, "NEWLINE") is True:
            return False, 0
        if context.check_token(i, "LPARENTHESIS") is True:
            nest += 1
            i += 1
            return self.find_nest_content(context, nest, i)
        return False, 0
