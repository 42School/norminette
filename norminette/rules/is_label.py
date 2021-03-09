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
        i += 1
        i = context.skip_ws(i)
        if context.check_token(i, "COLON") is False:
            return False, 0
        while context.peek_token(i) and context.check_token(i, "NEWLINE") is False:
            i += 1
        i = context.eol(i)
        return True, i
