from norminette.rules import Rule


class CheckLineLen(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = []

    def run(self, context):
        """
        Lines must not be over 80 characters long
        """
        i = 0
        line_too_long = {}
        for tkn in context.tokens[: context.tkn_scope]:
            if tkn.pos[1] > 81 and tkn.pos[0] not in line_too_long:
                context.new_error("LINE_TOO_LONG", tkn)
                line_too_long[tkn.pos[0]] = True
            i += 1
        return False, 0
