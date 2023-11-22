from norminette.rules import Rule, Primary


class IsTernary(Rule, Primary, priority=53):
    def run(self, context):
        """
        Catches ternaries and raises an error
        """
        i = 0
        while context.peek_token(i) is not None and context.check_token(i, ["SEMI_COLON", "NEWLINE"]) is False:
            if context.check_token(i, "TERN_CONDITION") is True:
                while context.peek_token(i) is not None and context.check_token(i, ["SEMI_COLON", "NEWLINE"]) is False:
                    i += 1
                i += 1
                i = context.eol(i)
                return True, i
            i += 1
        return False, 0
