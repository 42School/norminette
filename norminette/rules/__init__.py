import importlib
import os
from .rule import Rule
from glob import glob

path = os.path.dirname(os.path.realpath(__file__))
files = glob(path + "/check_*.py")

rules = {}
primary_rules = {}

for f in files:
    mod_name = f.split('/')[-1].split('.')[0]
    class_name = "".join([s.capitalize() for s in mod_name.split('_')])
    module = importlib.import_module("rules." + mod_name)
    rule = getattr(module, class_name)
    rule = rule()
    if rule.primary is True:
        primary_rules[rule.name] = rule
    rules[class_name] = rule
