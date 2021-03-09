from norminette.rules import PrimaryRule


class IsDeclaration(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 5
        self.scope = []

    def run(self, context):
        # return False, 0
        i = context.skip_ws(0, nl=False)
        p = 0
        ident = None
        while context.peek_token(i) is not None and context.check_token(i, "SEMI_COLON") is False:
            if context.check_token(i, "LPARENTHESIS"):
                p += 1
            if context.check_token(i, "RPARENTHESIS"):
                p -= 1
            if context.check_token(i, ["IDENTIFIER", "NULL"]):
                ident = context.peek_token(i)
            i += 1
        i += 1
        i = context.skip_ws(i, nl=False)
        if context.check_token(i, "NEWLINE"):
            i += 1
        if p == 0 and ident != None:
            return True, i
        return False, 0
