from norminette.rules import Rule


class CheckTernary(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = []

    def run(self, context):
        """
        Ternaries are forbidden
        """
        for i in range(0, context.tkn_scope):
            if context.check_token(i, "TERN_CONDITION") is True:
                context.new_error("TERNARY_FBIDDEN", context.peek_token(i))
        return False, 0
