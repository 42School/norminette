import os
from functools import cmp_to_key
from typing import Optional, Union, Literal

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


class File:
    def __init__(self, path: str, source: Optional[str] = None) -> None:
        self.path = path
        self._source = source

        self.errors = Errors()
        self.basename = os.path.basename(path)
        self.name, self.type = os.path.splitext(self.basename)

    @property
    def source(self) -> str:
        if not self._source:
            with open(self.path) as file:
                self._source = file.read()
        return self._source

    def __repr__(self) -> str:
        return f"<File {self.path!r}>"
