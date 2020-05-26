import rules
from context import Context
from functools import cmp_to_key
from exceptions import CParsingError





def sort_errs(a, b):
    return a.col - b.col if a.line == b.line else a.line - b.line


class Registry:
    global has_err
    def __init__(self):
        self.rules = rules.rules
        self.primary_rules = rules.primary_rules
        self.dependencies = {}
        for k, r in self.rules.items():
            r.register(self)

    def run_rules(self, context, rule):
        ret, read = rule.run(context)
#        print(context.history, context.tokens[:5], rule)
        if ret is True:
            if rule.name.startswith("Is"):
                context.tkn_scope = read
                context.history.append(rule.name)
            for r in self.dependencies.get(rule.name, []):
                self.run_rules(context, self.rules[r])
            if 'all' in self.dependencies:
                for r in self.dependencies['all']:
                    self.run_rules(context, self.rules[r])
            #context.history.pop(-1)
            context.tkn_scope = 0
        return ret, read

    def run(self, context, source):
        unrecognized_tkns = []
        while context.tokens != []:
            context.tkn_scope = len(context.tokens)
            for rule in self.primary_rules:
                if type(context.scope) not in rule.scope and rule.scope != []:
                    continue
                ret, jump = self.run_rules(context, rule)
                if ret is True:
                    if unrecognized_tkns != []:
                        print ('uncaught -> ', context.filename)
                        print ('uncaught -> ', unrecognized_tkns)
                        unrecognized_tkns = []
                    context.dprint(rule.name, jump)
                    context.update()
                    context.pop_tokens(jump)
                    break
            # #############################################################
            else:  # Remove these one ALL  primary rules are done
                    # print("#, ", context.tokens[0])
                unrecognized_tkns.append(context.tokens[0])
                context.pop_tokens(1)  # ##################################
            # #############################################################
        if unrecognized_tkns != []:
            print ("uncaught ->", unrecognized_tkns)
            #raise CParsingError(f"Unrecognized line while parsing line {unrecognized_tkns[0].pos[0]}")
        if context.errors == []:
            print(context.filename + ": OK!")
        else:
            print(context.filename + ": KO!")
            context.errors = sorted(context.errors, key=cmp_to_key(sort_errs))
            for err in context.errors:
                print(err)
