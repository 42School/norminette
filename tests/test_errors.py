import json
from typing import List
from dataclasses import astuple

import pytest

from norminette.file import File
from norminette.lexer import Lexer
from norminette.context import Context
from norminette.registry import Registry
from norminette.errors import JSONErrorsFormatter
from norminette.errors import Error, Errors, Highlight as H

tests = [
    {
        "file": File("/nium/test.c", "int\tmain()\n{\n\treturn ;\n}\n"),
        "test": {
            "files": [
                {
                    "path": "/nium/test.c",
                    "status": "Error",
                    "errors": [
                        {
                            "name": "INVALID_HEADER",
                            "text": "Missing or invalid 42 header",
                            "level": "Error",
                            "highlights": [{"lineno": 1, "column": 1, "length": None, "hint": None}],
                        },
                        {
                            "name": "NO_ARGS_VOID",
                            "text": "Empty function argument requires void",
                            "level": "Error",
                            "highlights": [{"lineno": 1, "column": 10, "length": None, "hint": None}],
                        },
                    ],
                },
            ],
        },
    },
]


@pytest.mark.parametrize("file,test", [it.values() for it in tests])
def test_json_formatter_errored_file(file, test):
    lexer = Lexer(file)
    context = Context(file, lexer.get_tokens())
    Registry().run(context)

    formatter = JSONErrorsFormatter(file)
    assert str(formatter) == json.dumps(test, separators=(',', ':'))


def test_error_from_name():
    Error.from_name("NO_ARGS_VOID")
    with pytest.raises(KeyError):
        Error.from_name("KeyThatDoesNoExists")


@pytest.mark.parametrize("errors", [
    [
        Error("BAD_NAME", "Names can't be started with an '_'", "Error", [H(3, 5, 5)]),
        Error("GLOBAL_VAR", "Global variables detected, take care", "Notice", [H(2, 1, 1)]),
        Error("test", "ola", "Error", [H(1, 1, 1)]),
    ],
])
def test_add_error_signature(errors: List[Error]):
    sequence = Errors()

    for error in errors:
        sequence.add(error)

    assert len(sequence) == len(errors)
    assert list(errors) == errors


@pytest.mark.parametrize("args, kwargs", [
    [["NO_ARGS_VOID",], {"highlights": [H(1, 1, 2)]}],
])
def test_add_name_signature(args, kwargs):
    assert isinstance(args, list) and len(args) == 1
    assert set() == set(kwargs) - {"level", "highlights"}

    errors = Errors()
    errors.add(*args, **kwargs)


def test_error_add_highlight():
    highlights = [
        H(lineno=1, column=1, length=1),
        H(lineno=1, column=2, length=1),
    ]

    error = Error("42", "42")
    error.add_highlight(highlights[0])
    error.add_highlight(*astuple(highlights[1]))

    assert error.highlights == highlights
