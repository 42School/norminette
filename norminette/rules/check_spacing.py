from rules import Rule


class CheckSpacing(Rule):
    def run(self, context):
        i = 0
        while i < len(context.tokens[:context.tkn_scope]):
            if context.peek_token(i).type == "SPACE":
                i += 1
                if context.peek_token(i).type == "SPACE":
                    context.new_error(1001, context.peek_token(i - 1))
                    while context.peek_token(i) is not None\
                            and context.peek_token(i).type == "SPACE":
                        i += 1
            else:
                i += 1
        return True, 0
