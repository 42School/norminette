from typing import Dict, Any, List

import pytest
from _pytest.mark.structures import ParameterSet

from norminette.file import File
from norminette.lexer import Lexer


def lexer_from_source(source: str, /) -> Lexer:
    file = File("<file>", source)
    return Lexer(file)


def dict_to_pytest_param(data: Dict[str, List[Any]]) -> List[ParameterSet]:
    params: List[ParameterSet] = []
    for id, values in data.items():
        param = pytest.param(*values, id=id)
        params.append(param)
    return params
