import importlib
import os
from operator import attrgetter

from norminette.rules.rule import Rule, Primary, Check


class Rules:
    __slots__ = (
        "all",
        "primaries",
        "checks",
    )

    __instance = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        path = os.path.dirname(os.path.realpath(__file__))
        for f in os.listdir(path):
            name, _ = os.path.splitext(f)
            importlib.import_module("norminette.rules." + name)

        self.all = Rule.__subclasses__()
        self.checks = Check.__subclasses__()
        self.primaries = sorted(Primary.__subclasses__(), reverse=True, key=attrgetter("priority"))
