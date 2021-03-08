from norminette.rules import Rule


class CheckDeclaration(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsDeclaration"]

    def run(self, context):
        """
        Checks for nl in declarations
        """
        # i = context.skip_ws(0)
        # while context.peek_token(i) and context.check_token(i, "SEMI_COLON") is False:
        # if context.check_token(i, "NEWLINE") is True:
        # context.new_error("NEWLINE_IN_DECL", context.peek_token(i))
        # i += 1
        return False, 0
