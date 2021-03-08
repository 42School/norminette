from norminette.rules import Rule

allowed_on_comment = ["COMMENT", "MULT_COMMENT", "SPACE", "TAB"]


class CheckComment(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = []

    def run(self, context):
        """
        Comments are only allowed in GlobalScope.
        """
        i = context.skip_ws(0)
        has_comment = False
        while context.peek_token(i) is not None and context.check_token(i, "NEWLINE") is False:
            if context.check_token(i, allowed_on_comment) is False:
                if has_comment == True:
                    context.new_error("COMMENT_ON_INSTR", context.peek_token(i))
                    return True, i
            elif context.check_token(i, ["COMMENT", "MULT_COMMENT"]) is True:
                if context.scope.name != "GlobalScope" or context.history[-1] == "IsFuncDeclaration":
                    context.new_error("WRONG_SCOPE_COMMENT", context.peek_token(i))
                has_comment = True
            i += 1
        i = context.skip_ws(0)
        return False, 0
