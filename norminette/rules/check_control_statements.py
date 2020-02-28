from rules import PrimaryRule


cs_keywords = ["DO", "WHILE", "FOR", "IF", "ELSE", "SWITCH"]


class CheckControlStatements(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 10

    def run(self, context):
        i = self.skip_ws(context, 0)
        if context.check_token(i, cs_keywords) is False:
            return False, 0

        i += 1
        i = self.skip_ws(context, i)
        if context.check_token(i, "LPARENTHESIS") is False:
            return False, 0
        i = self.skip_nested_par(context, i)
        i += 1
        while context.peek_token(i) is not None:
            if context.check_token(i, ["RBRACE", "NEWLINE"]) is True:
                break
            i += 1
        else:
            return False, 0
        i += 1
        return True, i
