from __future__ import annotations

import os
import json
from dataclasses import dataclass, field, asdict
from functools import cmp_to_key
from typing import TYPE_CHECKING, Sequence, Union, Literal, Optional, List

from norminette.norm_error import NormError, NormWarning, errors as errors_dict

if TYPE_CHECKING:
    from norminette.file import File


def sort_errs(a: Error, b: Error):
    # TODO Add to Error and Highlight dataclasses be sortable to remove this fn
    ah: Highlight = a.highlights[0]
    bh: Highlight = b.highlights[0]
    if ah.column == bh.column and ah.lineno == bh.lineno:
        return 1 if a.name > b.name else -1
    return ah.column - bh.column if ah.lineno == bh.lineno else ah.lineno - bh.lineno


@dataclass
class Highlight:
    lineno: int
    column: int
    length: Optional[int] = field(default=None)
    hint: Optional[str] = field(default=None)


@dataclass
class Error:
    name: str
    text: str
    level: Literal["Error", "Notice"]
    highlights: List[Highlight]


class Errors:
    __slots__ = "_inner"

    def __init__(self) -> None:
        self._inner = []

    def __len__(self) -> int:
        return len(self._inner)

    def __iter__(self):
        self._inner.sort(key=cmp_to_key(sort_errs))
        return iter(self._inner)

    # TODO Add `add(...)` method to allow creating `Highlight`s and `Error`s easily

    @property
    def status(self) -> Literal["OK", "Error"]:
        return "OK" if all(it.level == "Notice" for it in self._inner) else "Error"

    def append(self, value: Union[NormError, NormWarning]) -> None:
        # TODO Remove NormError and NormWarning since it does not provide `length` data
        assert isinstance(value, (NormError, NormWarning))
        level = "Error" if isinstance(value, NormError) else "Notice"
        value = Error(value.errno, value.error_msg, level, highlights=[
            Highlight(value.line, value.col, None),
        ])
        self._inner.append(value)


class _formatter:
    def __init__(self, files: Union[File, Sequence[File]]) -> None:
        if not isinstance(files, list):
            files = [files]
        self.files = files

    def __init_subclass__(cls) -> None:
        cls.name = cls.__name__.rstrip("ErrorsFormatter").lower()


class HumanizedErrorsFormatter(_formatter):
    def __str__(self) -> str:
        output = ''
        for file in self.files:
            output += f"{file.basename}: {file.errors.status}!"
            for error in file.errors:
                brief = errors_dict.get(error.name, "Error not found")
                highlight = error.highlights[0]
                output += f"\n{error.level}: {error.name:<20} "
                output += f"(line: {highlight.lineno:>3}, col: {highlight.column:>3}):\t{brief}"
        return output


class JSONErrorsFormatter(_formatter):
    def __str__(self):
        files = []
        for file in self.files:
            files.append({
                "path": os.path.abspath(file.path),
                "status": file.errors.status,
                "errors": tuple(map(asdict, file.errors)),
            })
        output = {
            "files": files,
        }
        return json.dumps(output, separators=",:")


formatters = (
    JSONErrorsFormatter,
    HumanizedErrorsFormatter,
)
