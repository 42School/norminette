import pytest

from norminette.file import File
from norminette.lexer import Lexer, TokenError

constants = (
    ("42", "<CONSTANT=42>\n"),
    ("+42", "<PLUS><CONSTANT=42>\n"),
    ("-42", "<MINUS><CONSTANT=42>\n"),
    ("+-42", "<PLUS><MINUS><CONSTANT=42>\n"),
    ("4.2", "<CONSTANT=4.2>\n"),
    (".42", "<CONSTANT=.42>\n"),
    ("4e2", "<CONSTANT=4e2>\n"),
    (".4e2", "<CONSTANT=.4e2>\n"),
    ("4e2f", "<CONSTANT=4e2f>\n"),
    (".4e2f", "<CONSTANT=.4e2f>\n"),
    ("042", "<CONSTANT=042>\n"),
    ("0x42", "<CONSTANT=0x42>\n"),
    ("-0x4e2", "<MINUS><CONSTANT=0x4e2>\n"),
    ("42l", "<CONSTANT=42l>\n"),
    ("42ul", "<CONSTANT=42ul>\n"),
    ("42ll", "<CONSTANT=42ll>\n"),
    ("42ull", "<CONSTANT=42ull>\n"),
    ("42u", "<CONSTANT=42u>\n"),
    ("-+-+-+-+-+-+-+-0Xe4Ae2", "<MINUS><PLUS><MINUS><PLUS><MINUS><PLUS><MINUS><PLUS><MINUS><PLUS><MINUS><PLUS><MINUS><PLUS><MINUS><CONSTANT=0Xe4Ae2>\n"),
    (".e42", "<DOT><IDENTIFIER=e42>\n"),
    ("4.4.4", None),
    ("4e4e4", None),
    ("4x4x4", None),
    ("42uul", None),
    ("42Lllu", None),
    ("42lul", None),
    (".42e", None),
)


@pytest.mark.parametrize("lexeme,expected", constants)
def test_constants_tokens(lexeme, expected):
    lexer = Lexer(File("<file>", lexeme))
    if expected is None:
        with pytest.raises(TokenError):
            lexer.get_next_token()
        return
    assert lexer.check_tokens() == expected
