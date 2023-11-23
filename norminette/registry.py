import collections
from functools import cmp_to_key
from operator import attrgetter

from norminette.rules import Rules, Primary
from norminette.exceptions import CParsingError

rules = Rules()


def sort_errs(a, b):
    if a.col == b.col and a.line == b.line:
        return 1 if a.errno > b.errno else -1
    return a.col - b.col if a.line == b.line else a.line - b.line


class Registry:
    global has_err

    def __init__(self):
        self.dependencies = collections.defaultdict(list)
        for rule in rules.checks:
            rule.register(self)
        for name, dependencies in self.dependencies.items():
            self.dependencies[name] = sorted(dependencies, reverse=True, key=attrgetter("__name__"))

    def run_rules(self, context, rule):
        rule = rule(context)
        result = rule.run(context)
        ret, read = result if isinstance(rule, Primary) else (False, 0)
        if ret:
            context.scope.instructions += 1
            if isinstance(rule, Primary):
                context.tkn_scope = read
                context.history.append(rule)
            for rule in self.dependencies[rule.name]:
                self.run_rules(context, rule)
            for rule in self.dependencies["_rule"]:
                self.run_rules(context, rule)
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
        context.state = "starting"
        for rule in self.dependencies["_start"]:
            self.run_rules(context, rule)
        context.state = "running"
        while context.tokens != []:
            context.tkn_scope = len(context.tokens)
            for rule in rules.primaries:
                if rule.scope and context.scope not in rule.scope:
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
        context.state = "ending"
        for rule in self.dependencies["_end"]:
            self.run_rules(context, rule)
        if unrecognized_tkns != []:
            print(context.debug)
            if context.debug > 0:
                print("uncaught ->", unrecognized_tkns)
        if context.errors == []:
            print(context.filename + ": OK!")
            for warning in sorted(context.warnings, key=cmp_to_key(sort_errs)):
                print(warning)
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
