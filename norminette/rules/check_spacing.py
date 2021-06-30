from norminette.rules import Rule


class CheckSpacing(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = []

    def run(self, context):
        """
        Indentation (except for preprocessors) must be done with tabs
        There cannot be trailing spaces or tabs at the end of line
        """
        i = 0
        if context.history[-1] == "IsEmptyLine":
            return False, 0
        space_tab_error = False
        space_error = False
        while i in range(len(context.tokens[: context.tkn_scope])):
            if context.check_token(i, "SPACE"):
                if context.peek_token(i).pos[1] == 1:
                    while i < context.tkn_scope and context.check_token(i, "SPACE"):
                        i += 1
                    if context.check_token(i + 1, "NEWLINE"):
                        context.new_error("SPACE_EMPTY_LINE", context.peek_token(i))
                        i += 1
                        continue
                    context.new_error("SPACE_REPLACE_TAB", context.peek_token(i))
                    continue
                i += 1
                if context.check_token(i, "SPACE"):
                    if space_error == False:
                        context.new_error("CONSECUTIVE_SPC", context.peek_token(i - 1))
                        space_error = True
                    while i < context.tkn_scope and context.check_token(i, "SPACE"):
                        i += 1
                if context.check_token(i, "NEWLINE"):
                    context.new_error("SPC_BEFORE_NL", context.peek_token(i - 1))
                if context.check_token(i, "TAB"):
                    if space_tab_error == False:
                        context.new_error("MIXED_SPACE_TAB", context.peek_token(i - 1))
                        space_tab_error = True
            elif context.check_token(i, ["TAB", "SPACE"]):
                if context.peek_token(i).pos[1] == 1:
                    while context.check_token(i, ["TAB", "SPACE"]):
                        i += 1
                    if context.check_token(i, "NEWLINE"):
                        context.new_error("SPC_BEFORE_NL", context.peek_token(i - 1))
                else:
                    i += 1
            else:
                i += 1
        return False, 0
