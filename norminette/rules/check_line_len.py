from rules import Rule


class CheckLineLen(Rule):
    def run(self, context):
        for tkn in context.tokens[:context.tkn_scope]:
            if tkn.type == "NEWLINE" and tkn.pos[1] > 81:
                context.new_error(1014, tkn)
