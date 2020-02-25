from rules import Rule


class CheckLineCount(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["CheckFuncDeclarations", "CheckBrace"]

    def run(self, context):
        if context.global_scope is True:
            if context.lines > 25:
                context.new_error(1021, context.tokens[context.tkn_scope])
            context.lines = 0
            return False, 0

        if context.global_scope is True:
            return False, 0

        if context.get_parent_rule() == "CheckBrace":
            if "LBRACE" in \
                    [t.type for t in context.tokens[:context.tkn_scope + 1]]:
                if context.global_scope is True:
                    return False, 0
            else:
                if context.scope_lvl == 0:
                    return False, 0

        for t in context.tokens[:context.tkn_scope + 1]:
            if t.type == "NEWLINE":
                context.lines += 1
        return False, 0
