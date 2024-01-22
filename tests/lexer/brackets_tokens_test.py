import pytest

from norminette.file import File
from norminette.lexer import Lexer

brackets = (
    ('{', "LBRACE"),
    ('}', "RBRACE"),
    ("(", "LPARENTHESIS"),
    (")", "RPARENTHESIS"),
    ("[", "LBRACKET"),
    ("]", "RBRACKET"),
)


@pytest.mark.parametrize("lexeme,name", brackets)
def test_brackets_tokens(lexeme, name):
    token = Lexer(File("<file>", lexeme)).get_next_token()
    assert token.type == name
