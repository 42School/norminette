from norminette.rules import PrimaryRule


class IsLabel(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 10

    def run(self, context):
        """
        Catches label and raises norm error whenever
        """
        i = context.skip_ws(0)
        if context.check_token(i, "IDENTIFIER") is False:
            return False, 0
        i = context.skip_ws(i + 1)  # +1 to skip the identifier
        if context.check_token(i, "COLON") is False:
            return False, 0
        i = context.skip_ws(i + 1)  # +1 to skip the colon
        if context.check_token(i, "NEWLINE"):
            return True, i
        while context.peek_token(i) and context.check_token(i, "SEMI_COLON") is False:
            i += 1
        i = context.eol(i + 1)  # +1 to skip the semi-colon
        return True, i
