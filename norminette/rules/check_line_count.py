from rules import Rule
from context import GlobalScope


class CheckLineCount(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["CheckFuncDeclarations", "CheckBrace"]

    def run(self, context):
        if type(context.scope) is GlobalScope:
            if context.get_parent_rule() == "CheckFuncDeclarations" \
                    and context.scope.lines > 25:
                context.new_error(1021, context.tokens[context.tkn_scope])
            return False, 0

        if context.get_parent_rule() == "CheckBrace":
            if "LBRACE" in \
                    [t.type for t in context.tokens[:context.tkn_scope + 1]]:
                if type(context.scope) is GlobalScope:
                    return False, 0
            else:
                if context.scope.lvl == 0:
                    return False, 0

        for t in context.tokens[:context.tkn_scope + 1]:
            if t.type == "NEWLINE":
                context.scope.lines += 1
        return False, 0
