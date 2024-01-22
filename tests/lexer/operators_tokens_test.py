import pytest

from norminette.file import File
from norminette.lexer import Lexer

operators = (
    (">>=", "RIGHT_ASSIGN"),
    ("<<=", "LEFT_ASSIGN"),
    ("+=", "ADD_ASSIGN"),
    ("-=", "SUB_ASSIGN"),
    ("*=", "MUL_ASSIGN"),
    ("/=", "DIV_ASSIGN"),
    ("%=", "MOD_ASSIGN"),
    ("&=", "AND_ASSIGN"),
    ("^=", "XOR_ASSIGN"),
    ("|=", "OR_ASSIGN"),
    ("<=", "LESS_OR_EQUAL"),
    (">=", "GREATER_OR_EQUAL"),
    ("==", "EQUALS"),
    ("!=", "NOT_EQUAL"),
    ("=", "ASSIGN"),
    (";", "SEMI_COLON"),
    (":", "COLON"),
    (",", "COMMA"),
    (".", "DOT"),
    ("!", "NOT"),
    ("-", "MINUS"),
    ("+", "PLUS"),
    ("*", "MULT"),
    ("/", "DIV"),
    ("%", "MODULO"),
    ("<", "LESS_THAN"),
    (">", "MORE_THAN"),
    ("...", "ELLIPSIS"),
    ("++", "INC"),
    ("--", "DEC"),
    ("->", "PTR"),
    ("&&", "AND"),
    ("||", "OR"),
    ("^", "BWISE_XOR"),
    ("|", "BWISE_OR"),
    ("~", "BWISE_NOT"),
    ("&", "BWISE_AND"),
    (">>", "RIGHT_SHIFT"),
    ("<<", "LEFT_SHIFT"),
    ("?", "TERN_CONDITION"),
)


@pytest.mark.parametrize("operator,type", operators)
def test_operators_tokens(operator, type):
    token = Lexer(File("<file>", operator)).get_next_token()
    assert token.type == type
