from rules import Rule


whitespaces = [
    "SPACE",
    "TAB",
    "NEWLINE"
]


class CheckBrace(Rule):
    def  __init__(self):
        super().__init__()
        self.primary = True
        self.dependencies = ["CheckSpacing", "CheckLineLen", "CheckLineIndent"]

    def skip_ws(self, context, pos):
        i = pos
        while context.peek_token(i) is not None \
                and context.peek_token(i).type in whitespaces:
            i += 1
        return i

    def run(self, context):
        i = self.skip_ws(context, 0)

        if context.peek_token(i) is None \
                or context.peek_token(i).type not in ["LBRACE", "RBRACE"]:
            return False, 0

        if context.peek_token(i) is not None \
                and context.peek_token(i).type == "LBRACE":
            context.indent_lvl += 1
        elif context.peek_token(i) is not None \
                and context.peek_token(i).type == "RBRACE":
            context.indent_lvl -= 1

        if context.peek_token(i).pos[1] > 1:
            """
            reverse list excluding brace, grab from list[0] to list[x] ='\n'
            check for anything else than whitespaces characters
            """
            li = []
            for t in context.tokens[i - 1::-1]:
                li.append(t)
                if t.type == "NEWLINE":
                    break
            if li is [] or li[0].pos[1] > 1:
                context.new_error(1013, context.peek_token(i))
                return True, i + 1

        for t in context.tokens[i + 1:]:
            if t.type == "NEWLINE":
                return True, i + 1
            elif t.type not in ["TAB", "SPACE"]:
                context.new_error(1013, context.peek_token(i))
                return True, i + 1
