import json

import pytest

from norminette.file import File
from norminette.lexer import Lexer
from norminette.context import Context
from norminette.registry import Registry
from norminette.errors import JSONErrorsFormatter

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
    assert str(formatter) == json.dumps(test, separators=",:")
