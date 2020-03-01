from rules import PrimaryRule
from context import Scope, GlobalScope


class CheckBrace(PrimaryRule):
    def __init__(self):
        super().__init__()

    def run(self, context):
        i = self.skip_ws(context, 0)

        if context.check_token(i, ["LBRACE", "RBRACE"]) is False:
            return False, 0

        j = i + 1

        while context.check_token(j, ["SPACE", "TAB"]):
            j += 1

        if context.peek_token(i) is not None \
                and context.peek_token(i).pos[1] > 1:
            """
            reverse list including brace, grab from list[0] to list[x] ='\n'
            check for anything else than whitespaces characters
            """
            li = []
            for t in context.tokens[i::-1]:
                if t.type == "NEWLINE":
                    break
                li.append(t)

            if li[0].pos[1] > 1:
                li.reverse()
                if li[0].type in ["SPACE", "TAB"] and li[0].pos[1] > 1:
                    context.new_error(1013, context.peek_token(i))
                    return True, j
                if len([t for t in li if t.type not in ["TAB", "SPACE"]]) > 1:
                    context.new_error(1013, context.peek_token(i))
                    return True, j

        for t in context.tokens[i + 1:]:
            if t.type == "NEWLINE":
                return True, j
            elif t.type not in ["TAB", "SPACE"]:
                context.new_error(1013, context.peek_token(i))
                return True, j

        return False, 0
