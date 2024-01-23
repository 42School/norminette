from functools import cmp_to_key
from typing import Union, Literal

from norminette.norm_error import NormError, NormWarning


def sort_errs(a, b):
    if a.col == b.col and a.line == b.line:
        return 1 if a.errno > b.errno else -1
    return a.col - b.col if a.line == b.line else a.line - b.line


class Errors:
    __slots__ = "_inner"

    def __init__(self) -> None:
        self._inner = []

    def __len__(self) -> int:
        return len(self._inner)

    def __iter__(self):
        self._inner.sort(key=cmp_to_key(sort_errs))
        return iter(self._inner)

    @property
    def status(self) -> Literal["OK", "Error"]:
        if not self:
            return "OK"
        if all(isinstance(it, NormWarning) for it in self):
            return "OK"
        return "Error"

    def append(self, value: Union[NormError, NormWarning]) -> None:
        assert isinstance(value, (NormError, NormWarning))
        self._inner.append(value)
