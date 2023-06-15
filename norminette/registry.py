from functools import cmp_to_key

import norminette.rules as rules
from norminette.exceptions import CParsingError


def sort_errs(a, b):
    if a.col == b.col and a.line == b.line:
        return 1 if a.errno > b.errno else -1
    return a.col - b.col if a.line == b.line else a.line - b.line


class Registry:
    global has_err

    def __init__(self):
        self.rules = rules.rules
        self.primary_rules = rules.primary_rules
        self.dependencies = {}
        for k, r in self.rules.items():
            r.register(self)
        for k, v in self.dependencies.items():
            self.dependencies[k] = sorted(self.dependencies[k], reverse=True)

    def run_rules(self, context, rule):
        if rule.name.startswith("Is"):
            ret, read = rule.run(context)
        else:
            # print (rule.name)
            ret = False
            read = 0
            rule.run(context)
        # print(context.history, context.tokens[:5], rule)
        # if rule.name.startswith("Is"):
        #     print (rule.name, ret)
        if ret is True:
            context.scope.instructions += 1
            if rule.name.startswith("Is"):
                # print ("Line", context.tokens[0].pos[0], rule.name)
                context.tkn_scope = read
                context.history.append(rule.name)
            for r in self.dependencies.get(rule.name, []):
                self.run_rules(context, self.rules[r])
            if "all" in self.dependencies:
                for r in self.dependencies["all"]:
                    self.run_rules(context, self.rules[r])
            # context.history.pop(-1)
            context.tkn_scope = 0
        return ret, read

    def run(self, context, source):
        """
        Main function for each file.
        Primary rules are determined by the prefix "Is" and
        are run by order of priority as defined in each class
        Each secondary rule is then run in arbitrary order based on their
        dependencies
        """
        unrecognized_tkns = []
        while context.tokens != []:
            context.tkn_scope = len(context.tokens)
            for rule in self.primary_rules:
                if type(context.scope) not in rule.scope and rule.scope != []:
                    continue
                ret, jump = self.run_rules(context, rule)
                if ret is True:
                    if unrecognized_tkns != []:
                        if context.debug == 0:
                            raise CParsingError(
                                f"Error: Unrecognized line {unrecognized_tkns[0].pos} while parsing line {unrecognized_tkns}"  # noqa: E501
                            )
                        print("uncaught -> ", context.filename)
                        print("uncaught -> ", unrecognized_tkns)
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
            print(context.debug)
            if context.debug > 0:
                print("uncaught ->", unrecognized_tkns)
        if context.errors == []:
            print(context.filename + ": OK!")
        else:
            print(context.filename + ": Error!")
            context.errors = sorted(
                context.errors + context.warnings, key=cmp_to_key(sort_errs)
            )
            for err in context.errors:
                print(err)
            # context.warnings = sorted(context.warnings, key=cmp_to_key(sort_errs))
            # for warn in context.warnings:
            #     print (warn)
