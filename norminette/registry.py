import importlib, os
from glob import glob
from context import Context


class Registry:
    def __init__(self):
        self.rules = {}
        self.primary_rules = {}
        self.registry = {}
        self.get_rules()

    def get_rules(self):
        path = os.path.dirname(os.path.realpath(__file__))
        files = glob(path + "/rules/check_*.py")
        for f in files:
            mod_name = f.split('/')[-1].split('.')[0]
            class_name = "".join([s.capitalize() for s in mod_name.split('_')])
            module = importlib.import_module("rules." + mod_name)
            rule = getattr(module, class_name)
            rule = rule()
            if rule.primary is True:
                self.primary_rules[rule.name] = rule
            self.rules[class_name] = rule
            self.registry[class_name] = self.rules[class_name].subrules

    def run(self, context):
        while context.tokens != []:
            for name, rule in self.primary_rules.items():
                jump = 0
                ret, jump = rule.run(context)
                if ret is True:
                    # print(context.tokens[0:jump])
                    self.apply_depedencies(name, context)
                    context.pop_tokens(jump)
                    break
                else:
                    context.pop_tokens(1)

    def apply_dependencies(self, rulename, context):
        for d in self.registry[rulename]:
            self.rules[d].run(context)
            self.apply_dependencies(self.rules[d].name, context)
        pass
