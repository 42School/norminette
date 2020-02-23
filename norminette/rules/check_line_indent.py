from rules import Rule


class CheckLineIndent(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["CheckFuncDeclarations"]

    def run(self, context):
        lines = [[]]
#        print("tokens:", context.tokens[:context.tkn_scope + 1])
        for t in context.tokens[:context.tkn_scope]:
            if t.type == "NEWLINE":
                lines.append([])
            else:
                lines[-1].append(t)

        lines = [li for li in lines if li != []]

        z=0
        for l in lines:
#            print(l, z)
#            z+=1
            if len(l) > 0 and l[0].pos[1] > 1:
                continue
            else:
                lvl = context.indent_lvl
                i = 0
                while i in range(len(l)):
                    if l[i].type == "TAB":
                        lvl -= 1
                        i += 1
                        continue
                    elif l[i].type == "LBRACE":
                        lvl -= 1
                        break
                    break
                if lvl > 0:
                    context.new_error(1019, l[i])
                elif lvl < 0:
                    context.new_error(1020, l[i])
        return False, 0
