from __future__ import annotations

import os
import json
from dataclasses import dataclass, field, asdict
from typing import (
    TYPE_CHECKING,
    Sequence,
    Union,
    Literal,
    Optional,
    List,
    Any,
)

from norminette.norm_error import NormError, NormWarning, errors as errors_dict

if TYPE_CHECKING:
    from norminette.file import File


@dataclass
class Highlight:
    lineno: int
    column: int
    length: Optional[int] = field(default=None)
    hint: Optional[str] = field(default=None)

    def __lt__(self, other: Any) -> bool:
        assert isinstance(other, Highlight)
        if self.lineno == other.lineno:
            if self.column == other.column:
                return len(self.hint or '') > len(other.hint or '')
            return self.column > other.column
        return self.lineno > other.lineno


@dataclass
class Error:
    name: str
    text: str
    level: Literal["Error", "Notice"] = field(default="Error")
    highlights: List[Highlight] = field(default_factory=list)

    @classmethod
    def from_name(cls: Type[Error], /, name: str, **kwargs) -> Error:
        return cls(name, errors_dict[name], **kwargs)

    def __lt__(self, other: Any) -> bool:
        assert isinstance(other, Error)
        if not self.highlights:
            return bool(other.highlights) or self.name > other.name
        if not other.highlights:
            return bool(self.highlights) or other.name > self.name
        ah, bh = min(self.highlights), min(other.highlights)
        if ah.column == bh.column and ah.lineno == bh.lineno:
            return self.name < other.name
        return (ah.lineno, ah.column) < (bh.lineno, bh.column)


class Errors:
    __slots__ = "_inner"

    def __init__(self) -> None:
        self._inner = []

    def __len__(self) -> int:
        return len(self._inner)

    def __iter__(self):
        self._inner.sort()
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
    name: str

    def __init__(self, files: Union[File, Sequence[File]]) -> None:
        if not isinstance(files, Sequence):
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
        return json.dumps(output, separators=(',', ':'))


formatters = (
    JSONErrorsFormatter,
    HumanizedErrorsFormatter,
)
