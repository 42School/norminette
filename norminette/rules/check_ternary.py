from norminette.rules import Rule, Check


class CheckTernary(Rule, Check):
    def run(self, context):
        """
        Ternaries are forbidden
        """
        for i in range(0, context.tkn_scope):
            if context.check_token(i, "TERN_CONDITION") is True:
                context.new_error("TERNARY_FBIDDEN", context.peek_token(i))
        return False, 0
