from norminette.rules import Rule, Primary


class IsComment(Rule, Primary, priority=90):
    def run(self, context):
        """
        Catches comments tokens
        """
        i = context.skip_ws(0)
        if context.check_token(i, ["MULT_COMMENT", "COMMENT"]) is True:
            self.comment = context.peek_token(i)
            i += 1
            i = context.eol(i)
            return True, i
        return False, 0
