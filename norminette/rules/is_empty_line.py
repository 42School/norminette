from norminette.rules import Rule, Primary

cs_keywords = ["DO", "WHILE", "FOR", "IF", "ELSE", "SWITCH"]
whitespaces = ["TAB", "SPACE", "NEWLINE"]


class IsEmptyLine(Rule, Primary, priority=70):
    def run(self, context):
        """
        Catches empty line
        BUG: Catches end of line token on unrecognized line
        """
        i = 0
        while context.check_token(i, ["SPACE", "TAB"]) is True:
            i += 1
        if context.check_token(i, "NEWLINE") is True or context.peek_token(i) is None:
            i = context.eol(i)
            return True, i
        return False, 0
