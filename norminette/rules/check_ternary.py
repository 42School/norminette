from norminette.rules import Rule


class CheckTernary(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsTernary"]

    def run(self, context):
        """
        Ternaries are forbidden
        """
        context.new_error("TERNARY_FBIDDEN", context.peek_token(0))
        return False, 0
