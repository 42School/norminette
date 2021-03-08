from norminette.rules import PrimaryRule


class IsComment(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 90
        self.scope = []

    def run(self, context):
        """
        Catches comments tokens
        """
        i = context.skip_ws(0)
        if context.check_token(i, ["MULT_COMMENT", "COMMENT"]) is True:
            i += 1
            i = context.eol(i)
            return True, i
        return False, 0
