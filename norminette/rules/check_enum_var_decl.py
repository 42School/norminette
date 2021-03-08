from norminette.rules import Rule


class CheckEnumVarDecl(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsEnumVarDecl"]

    def run(self, context):
        """
        Checks for nl in declarations
        """
        i = context.skip_ws(0)
        while context.peek_token(i) and context.check_token(i, "COMMA") is False:
            if context.check_token(i, "NEWLINE") is True:
                i += 1
                while context.peek_token(i) is not None and context.check_token(i, "NEWLINE") is False:
                    if context.check_token(i, "LBRACE") is True:
                        return False, 0
                    i += 1
                # context.new_error("NEWLINE_IN_DECL", context.peek_token(i))
                return True, i
            i += 1
        return False, 0
