import importlib
from glob import glob


class Rules:
    def __init__(self):
        self.rules = []
        self.getRules()
        pass

    def getRules(self):
        files = glob('rules/*.py')
        for f in files:
            mod_name = f.split('/')[1].split('.')[0]
            class_name = "".join([s.capitalize() for s in mod_name.split('_')])
            if class_name != 'Init':
                path = "rules." + mod_name
                module = importlib.import_module(path)
                rule = getattr(module, class_name)
                self.rules.append(rule)
# This is just for testing
                rule().run()

    def run(self, tokens):
        error = False
        for rule in self.rules:
            error = True if rule().run() else error
        return error
