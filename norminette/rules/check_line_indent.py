from rules import Rule


class CheckLineIndent(Rule):
    def run(self, context):
        lines = [[]]
        for t in context.tokens[:context.tkn_scope]:
            if t.type == "NEWLINE":
                lines[-1].append(t)
                lines.append([])
            else:
                lines[-1].append(t)

        if lines[-1] == []:
            lines = lines[:-1]

        for l in lines:
            if len(l) > 0 and l[0].pos[1] > 1:
                continue
            else:
                lvl = context.indent_lvl
                for i in range(len(l)):
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
