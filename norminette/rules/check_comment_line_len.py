from norminette.rules import Rule


class CheckCommentLineLen(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsComment"]

    def run(self, context):
        """
        Lines must not be over 80 characters long
        """
        i = 0
        while context.check_token(i, ["COMMENT", "MULT_COMMENT"]) is False:
            i += 1
        val = context.peek_token(i).value
        line_start = context.peek_token(0).pos[1]
        val = val.split("\n")
        for item in val:
            if len(item) + line_start > 81:
                context.new_error("LINE_TOO_LONG", context.peek_token(0))
            line_start = 0
