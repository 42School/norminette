from norminette.rules import Rule


class CheckLabel(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = []

    def run(self, context):
        """
        Goto and labels are forbidden
        """
        i = 0
        if context.scope.name not in ("Function", "ControlStructure"):
            return False, 0
        i = context.skip_ws(i)
        if context.check_token(i, "GOTO"):
            context.new_error("GOTO_FBIDDEN", context.peek_token(0))
            return False, 0
        if context.check_token(i, "IDENTIFIER") is False:
            return False, 0
        i = context.skip_ws(i + 1)
        if context.check_token(i, "COLON"):
            context.new_error("LABEL_FBIDDEN", context.peek_token(0))
        return False, 0
