import pytest

from norminette.file import File
from norminette.lexer import Lexer, TokenError

char_constants = (
    ("'*'", "<CHAR_CONST='*'>"),
    ("'\\n'", "<CHAR_CONST='\\n'>"),
    ("'\\042'", "<CHAR_CONST='\\042'>"),
    ("'0x042'", "<CHAR_CONST='0x042'>"),
    ("'\n1'", None),
    ("'\\n\n'", None),
    ("'A", None),
)


@pytest.mark.parametrize("lexeme,expected", char_constants)
def test_char_constants_tokens(lexeme, expected):
    lexer = Lexer(File("<file>", lexeme))
    if expected is None:
        with pytest.raises(TokenError):
            lexer.get_next_token()
        return
    token = lexer.get_next_token()
    assert token.test() == expected
