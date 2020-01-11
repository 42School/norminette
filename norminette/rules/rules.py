import importlib
import os
from glob import glob
from .context import Context


class Rules:
    def __init__(self):
        self.rules = []
        self.getRules()
        pass

    def getRules(self):
        path = os.path.dirname(os.path.realpath(__file__))
        files = glob(path + "/*_rule.py")
        for f in files:
            print(f)
            mod_name = f.split('/')[-1].split('.')[0]
            class_name = "".join([s.capitalize() for s in mod_name.split('_')])
            module = importlib.import_module("rules." + mod_name)
            rule = getattr(module, class_name)
            self.rules.append(rule)
        # This is just for testing
        # rule().run()

    def run(self, tokens, filename):
        error = False
        context = Context(filename)
        for i in range(len(tokens)):
            # print(tokens[i], end="" if tokens[i].type != "NEWLINE" else "\n")
            for rule in self.rules:
                ret, jump = rule(tokens[i:], context)
                if ret is True:
                    i += jump
                    break
        if context.errors != []:
            print(filename + ": KO!")
            for error in context.errors:
                print(error)
        else:
            print(filename + ": OK!")
        return
