import importlib
import os
from glob import glob


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

    def run(self, tokens):
        error = False
        for rule in self.rules:
            error = True if rule().run() else error
        return error
