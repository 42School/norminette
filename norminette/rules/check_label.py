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
        if context.scope.name != "Function":
            return False, 0
        while i < context.tkn_scope:
            if context.check_token(i, ["GOTO", "COLON"]):
                context.new_error("LABEL_FBIDDEN", context.peek_token(0))
                return False, 0
            i += 1
        return False, 0
