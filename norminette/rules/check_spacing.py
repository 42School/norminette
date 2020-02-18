from rules import Rule


class CheckSpacing(Rule):
    def run(self, context):
        i = 0
        while i in range(len(context.tokens[:context.tkn_scope])):
            if context.peek_token(i).type == "SPACE":
                if context.peek_token(i).pos[1] == 1:
                    if context.peek_token(i + 1) is not None \
                            and context.peek_token(i + 1).type == "NEWLINE":
                        context.new_error(1022, context.peek_token(i))
                        i += 1
                        continue
                    context.new_error(1000, context.peek_token(i))
                i += 1
                if context.peek_token(i).type == "SPACE":
                    context.new_error(1001, context.peek_token(i - 1))
                    while i < context.tkn_scope \
                            and context.peek_token(i) is not None \
                            and context.peek_token(i).type == "SPACE":
                        i += 1
                if context.peek_token(i) is not None \
                        and context.peek_token(i).type == "NEWLINE":
                    context.new_error(1023, context.peek_token(i - 1))
            elif context.peek_token(i).type == "TAB":
                if context.peek_token(i).pos[1] == 1:
                    while context.peek_token(i).type == "TAB":
                        i += 1
                    if context.peek_token(i).type == "NEWLINE":
                        context.new_error(1023, context.peek_token(i - 1))
                else:
                    """
                    Maybe check for correct tabs here as well?
                    """
                    i += 1
            else:
                i += 1
