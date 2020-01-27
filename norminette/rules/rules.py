import importlib
import os
from glob import glob
from context import Context


class Rules:
    def __init__(self):
        self.rules = {}
        self.registry = {}
        self.getRules()

    def getRules(self):
        path = os.path.dirname(os.path.realpath(__file__))
        files = glob(path + "/check_*.py")
        for f in files:
            mod_name = f.split('/')[-1].split('.')[0]
            class_name = "".join([s.capitalize() for s in mod_name.split('_')])
            module = importlib.import_module("rules." + mod_name)
            rule = getattr(module, class_name)
            self.rules[class_name] = rule()
            self.registry[class_name] = self.rules[class_name].subrules

    def run(self, tokens, filename, context):
        error = False
        i = 0
        while context.tokens != []:
            for rulename, rule in self.rules.items():
                jump = 0
                ret, jump = rule.run(context)
                if ret is True:
                    """
                    print(self.registry[rulename])
                    print(
                            f"{rulename} (line ({context.lines},",
                            f"{context.tokens[0]}) : {context.tokens[:jump]}"
                        )
                    """
                    break
            print(context.tokens[0:jump if jump > 0 else 1])
            context.popTokens(jump if jump > 0 else 1)
        if context.errors != []:
            print(filename + ": KO!")
            for error in context.errors:
                print(error)
        else:
            print(filename + ": OK!")
        return
