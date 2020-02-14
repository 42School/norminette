from rules import Rule


class CheckLineCount(Rule):
    def run(self, context):
        if context.global_scope is True:
            if context.lines > 25:
                context.new_error(1021, context.tokens[context.tkn_scope])
            context.lines = 0
            return

        if context.global_scope is True:
            return

        if context.get_parent_rule() == "CheckBrace":
            if "LBRACE" in \
                    [t.type for t in context.tokens[:context.tkn_scope + 1]]:
                if context.global_scope is True:
                    return
            else:
                if context.scope_lvl == 0:
                    return

        for t in context.tokens[:context.tkn_scope + 1]:
            if t.type == "NEWLINE":
                context.lines += 1
