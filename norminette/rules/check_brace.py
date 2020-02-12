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
        self.dependencies = [ "CheckLineLen"]

    def skip_ws(self, context, pos):
        i = pos
        while context.peek_token(i) is not None \
                and context.peek_token(i).type in whitespaces:
            i += 1
        return i

    def run(self, context):
        i = self.skip_ws(context, 0)
        err = False
        if context.peek_token(i) is not None \
                and context.peek_token(i).type in ["LBRACE", "RBRACE"]:
            if context.peek_token(i).type == "LBRACE":
                context.indent_lvl += 1
            else:
                context.indent_lvl -= 1
            if context.peek_token(i).pos[1] > 1:
                for tkn in context.tokens[:i]:
                    if tkn.type == "NEWLINE":
                        break
                    if tkn.type not in ["TAB", "SPACE"]:
                        context.new_error(1013, context.peek_token(i))
                        err = True
                        return True, i
                if context.peek_token(i).pos[1] > 1 and not err:
                    print("----------->", context.peek_token(i))
                    context.new_error(1013, context.peek_token(i))
                    err = True
            i += 1
            j = i
            while context.peek_token(j) is not None:
                if context.peek_token(j).type == "NEWLINE":
                    break
                elif context.peek_token(j).type in ["SPACE", "TAB"]:
                    j += 1
                elif not err:
                    context.new_error(1013, context.peek_token(i))
                    return True, i
                else:
                    return True, i
            return True, j
        return False, 0
