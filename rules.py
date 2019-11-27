import importlib
from glob import glob

# import rules.third_rule as third_rule

filenames = glob('rules/*.py')


for f in filenames:
    module_name = f.split('/')[1]
    f_name_parts = module_name.split('_')
    module_name = module_name.split('.')[0]
    f_name_parts[-1] = f_name_parts[-1].split('.')[0]
    c_name = "".join([file_part.capitalize() for file_part in f_name_parts])
    if c_name != 'Init':
        module_path = "rules." + module_name
        module = importlib.import_module(module_path)
        model = getattr(module, c_name)
        print(model().rule_func())
