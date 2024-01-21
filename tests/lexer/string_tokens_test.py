import pytest

from norminette.file import File
from norminette.lexer import Lexer

strings = (
    ('"Basic string"', '<STRING="Basic string">'),
    ('L"Basic string"', '<STRING=L"Basic string">'),
    ('"Basic \\"string\\""', '<STRING="Basic \\"string\\"">'),
    ('"Escaped \\\\\\"string\\\\\\\\\\"\\\\"', '<STRING="Escaped \\\\\\"string\\\\\\\\\\"\\\\">'),
)


@pytest.mark.parametrize("string,expected", strings)
def test_string_tokens(string, expected):
    token = Lexer(File("<file>", string)).get_next_token()
    assert token.test() == expected
