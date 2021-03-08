from norminette.rules import Rule


class CheckLineLen(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = []

    def run(self, context):
        """
        Lines must not be over 80 characters long
        """
        for tkn in context.tokens[: context.tkn_scope]:
            if tkn.type == "NEWLINE" and tkn.pos[1] > 81:
                context.new_error("LINE_TOO_LONG", tkn)
        return False, 0
