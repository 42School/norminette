__all__ = (
    "rules",
    "primary_rules",
    "Rule",
    "PrimaryRule",
)

import operator
import itertools
import importlib
import os

from norminette.rules.rule import PrimaryRule
from norminette.rules.rule import Rule


def partition(predicate, iterable):
    it1, it2 = itertools.tee(iterable)
    return itertools.filterfalse(predicate, it1), filter(predicate, it2)


path = os.path.dirname(os.path.realpath(__file__))

for f in os.listdir(path):
    name, _ = os.path.splitext(f)
    importlib.import_module("norminette.rules." + name)

_all_rules = Rule.__subclasses__()[1:] + PrimaryRule.__subclasses__()
_all_rules = map(type.__call__, _all_rules)  # In 3.11^ we can just use `operator.call``

_is_primary_rule = operator.attrgetter("primary")
_rules, _primary_rules = partition(_is_primary_rule, _all_rules)

rules = {rule.__class__.__name__: rule for rule in _rules}

primary_rules = sorted(_primary_rules, reverse=True, key=operator.attrgetter("priority"))
