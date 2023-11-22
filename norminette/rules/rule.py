from typing import Tuple

from norminette.context import Context


class Rule:
    __slots__ = ()

    def __new__(cls, context: Context, *args, **kwargs):
        cls.context = context
        cls.name = cls.__name__

        return super().__new__(cls, *args, **kwargs)

    def __repr__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, value) -> bool:
        if isinstance(value, str):
            return self.name == value
        if hasattr(value, "name"):
            return self.name == value.name
        return super().__eq__(value)

    def __ne__(self, value) -> bool:
        return not (self == value)


class Check:
    __slots__ = ()

    depends_on: Tuple[str, ...]

    runs_on_start: bool
    runs_on_rule: bool
    runs_on_end: bool

    def __init_subclass__(cls, **kwargs):
        if not hasattr(cls, "depends_on"):
            cls.depends_on = ()
        cls.runs_on_start = kwargs.pop("runs_on_start", getattr(cls, "runs_on_start", False))
        cls.runs_on_rule = kwargs.pop("runs_on_rule", getattr(cls, "runs_on_rule", not cls.depends_on))
        cls.runs_on_end = kwargs.pop("runs_on_end", getattr(cls, "runs_on_end", False))

    @classmethod
    def register(cls, registry):
        for rule in cls.depends_on:
            registry.dependencies[rule].append(cls)
        if cls.runs_on_start:
            registry.dependencies["_start"].append(cls)
        if cls.runs_on_rule:
            registry.dependencies["_rule"].append(cls)
        if cls.runs_on_end:
            registry.dependencies["_end"].append(cls)

    def is_starting(self):
        """Returns if this `Check` is being run before `Primary`.

        It is only called if `runs_on_start` is set to `True`.
        """
        return self.context.state == "starting"  # type: ignore

    def is_ending(self):
        """Returns if this `Check` is being run after all rules.

        It is only called if `runs_on_end` is set to `True`.
        """
        return self.context.state == "ending"  # type: ignore

    def run(self, context: Context) -> None:
        return


class Primary:
    __slots__ = ()

    priority: int
    scope: Tuple[str, ...]

    def __init_subclass__(cls, **kwargs):
        cls.priority = kwargs.pop("priority", 0)
        if not hasattr(cls, "scope"):
            cls.scope = ()

    def run(self, context: Context) -> Tuple[bool, int]:
        return False, 0
