from rules import Rule


class CheckLineIndent(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["CheckFuncDeclarations", "CheckVarDeclarations"]

    def run(self, context):
        lines = [[]]
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
                #elif l[i].type == "LBRACE":
                #    lvl -= 1
                break
            else:
                continue
            if lvl > 0:
                context.new_error(1019, l[i])
            elif lvl < 0:
                print(context.scope, context.scope.indent,  1020)
                context.new_error(1020, l[i])
        return False, 0
