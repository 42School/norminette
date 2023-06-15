from norminette.rules import Rule


class CheckNewlineIndent(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = [
            "IsDeclaration",
            "IsAssignation",
            "IsCast",
            "IsExpressionStatement",
        ]

    def run(self, context):
        """
        If a line has a newline inside, we must check for indent - authorized : same indent/same + 1 indent
        """
        if context.scope.name != "Function":
            return False, 0
        expected = context.scope.indent
        i = context.find_in_scope("NEWLINE", nested=False) + 1
        if i != -1 and i < context.tkn_scope - 2:
            start = i
            got = 0
            while context.check_token(start + got, "TAB"):
                got += 1
            if got > expected + 1:
                context.new_error("TOO_MANY_TAB", context.peek_token(start))
            if got < expected:
                context.new_error("TOO_FEW_TAB", context.peek_token(start))
        return False, 0
