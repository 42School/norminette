from rules import Rule
from scope import *



class CheckLineIndent(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = []

    def run(self, context):
        lines = [[]]
#        print("THEEERE")
        for t in context.tokens[:context.tkn_scope]:
            if t.type == "NEWLINE":
                lines.append([])
            else:
                lines[-1].append(t)

        lines = [li for li in lines if li != [] and li[0].pos[1] == 1]

        for l in lines:
            lvl = context.scope.indent
            for i in range(len(l)):
                if l[i].type == "TAB":
                    lvl -= 1
                    i += 1
                    continue
                break
            else:
                continue
            if lvl > 0:
                context.new_error("TOO_FEW_TAB", l[i])
            elif lvl < 0:
                context.new_error("TOO_MANY_TAB", l[i])
        return False, 0
