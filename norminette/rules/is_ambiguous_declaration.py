from norminette.rules import PrimaryRule

cs_keywords = ["DO", "WHILE", "FOR", "IF", "ELSE", "SWITCH", "CASE", "DEFAULT"]
whitespaces = ["TAB", "SPACE", "NEWLINE"]


class IsAmbiguousDeclaration(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 0
        self.scope = []

    def run(self, context):
        """
        Catches missing semi-colon or other various missing stuff. Dev feature
        """
        i = context.skip_ws(0, nl=False)
        while context.peek_token(i) and context.check_token(i, "NEWLINE") is False:
            if context.check_token(i, ["SEMI_COLON"]) is False:
                return False, 0
            i += 1
        return True, i
