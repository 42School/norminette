import importlib
from glob import glob

# import rules.third_rule as third_rule


class Rules:
    def __init__(self):
        self.rules = []
        self.getRules()
        print(self.rules)
        pass

    def getRules(self):
        filenames = glob('rules/*.py')


        for f in filenames:
            module_name = f.split('/')[1]
            f_name_parts = module_name.split('_')
            module_name = module_name.split('.')[0]
            f_name_parts[-1] = f_name_parts[-1].split('.')[0]
            c_name = "".join([file_part.capitalize()
                    for file_part in f_name_parts])
            if c_name != 'Init':
                module_path = "rules." + module_name
                module = importlib.import_module(module_path)
                rule = getattr(module, c_name)
                self.rules.append(rule)
                rule().rule_func()

Rules()
