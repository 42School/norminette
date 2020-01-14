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
        files = glob(path + "/check_*.py")
        for f in files:
            print(f)
            mod_name = f.split('/')[-1].split('.')[0]
            class_name = "".join([s.capitalize() for s in mod_name.split('_')])
            module = importlib.import_module("rules." + mod_name)
            rule = getattr(module, class_name)
            self.rules.append(rule())
        # This is just for testing
        # rule().run()

    def run(self, tokens, filename):
        error = False
        context = Context(filename, tokens)
        i = 0
        while context.tokens != []:
            # print(tokens[i], end="" if tokens[i].type != "NEWLINE" else "\n")
            for rule in self.rules:
                # print('i = ', str(i))
                # print('tokens[i] = ', tokens[i:])
                jump = 0
                ret, jump = rule.run(context)
                if ret is True:
                    break
            context.popTokens(jump if jump > 0 else 1)
        if context.errors != []:
            print(filename + ": KO!")
            for error in context.errors:
                print(error)
        else:
            print(filename + ": OK!")
        return
