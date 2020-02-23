from rules import Rule


class CheckSpacing(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["CheckFuncDeclarations"]

    def run(self, context):
        i = 0
        while i in range(len(context.tokens[:context.tkn_scope])):
            if context.check_token(i, "SPACE"):
                if context.peek_token(i).pos[1] == 1:
                    while i < context.tkn_scope \
                            and context.check_token(i, "SPACE"):
                        i += 1
                    if context.check_token(i + 1, "NEWLINE"):
                        context.new_error(1022, context.peek_token(i))
                        i += 1
                        continue
                    context.new_error(1000, context.peek_token(i))
                    continue
                i += 1
                if context.check_token(i, "SPACE"):
                    context.new_error(1001, context.peek_token(i - 1))
                    while i < context.tkn_scope \
                            and context.check_token(i, "SPACE"):
                        i += 1
                if context.check_token(i, "NEWLINE"):
                    context.new_error(1023, context.peek_token(i - 1))
            elif context.check_token(i, "TAB"):
                if context.peek_token(i).pos[1] == 1:
                    while context.check_token(i, "TAB"):
                        i += 1
                    if context.check_token(i, "NEWLINE"):
                        context.new_error(1023, context.peek_token(i - 1))
                else:
                    """
                    Maybe check for correct tabs here as well?
                    """
                    i += 1
            else:
                i += 1
        return False, 0
