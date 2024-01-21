import pytest

from norminette.file import File
from norminette.lexer import Lexer, TokenError


failed_tokens_tests = [
    {"text": "\tdouble f=45e++ai", "line": 1, "pos": 14},
    {"text": '\tchar *b = "e42\n\n', "line": 1, "pos": 15},
    {"text": "int\t\t\tn\t= 0x1uLl;", "line": 1, "pos": 19},
    {"text": 'char\t\t\t*yo\t\t\t= "', "line": 1, "pos": 31},
    {"text": "{return 1;}\\\\\\n", "line": 1, "pos": 12},
    {"text": "int a = a+++++a;\ndouble b = .0e4x;", "line": 2, "pos": 12},
    {"text": "int a = 1;\nint b = 10ul;\nint c = 10lul;\n", "line": 3, "pos": 9},
    {"text": "int number = 0x1uLl;", "line": 1, "pos": 14},
    {"text": "int number = 0x1ULl;", "line": 1, "pos": 14},
    {"text": "int number = 0x1lL;", "line": 1, "pos": 14},
    {"text": "int number = 0x1Ll;", "line": 1, "pos": 14},
    {"text": "int number = 0x1UlL;", "line": 1, "pos": 14},
    {"text": "int number = 10ullll", "line": 1, "pos": 14},
    {"text": "int number = 10lul", "line": 1, "pos": 14},
    {"text": "int number = 10lUl", "line": 1, "pos": 14},
    {"text": "int number = 10LUl", "line": 1, "pos": 14},
    {"text": "int number = 10uu", "line": 1, "pos": 14},
    {"text": "int number = 10Uu", "line": 1, "pos": 14},
    {"text": "int number = 10UU", "line": 1, "pos": 14},
    {"text": "int number = 0b0101e", "line": 1, "pos": 14},
    {"text": "int number = 0b0101f", "line": 1, "pos": 14},
    {"text": "int number = 0b0X101f", "line": 1, "pos": 14},
    {"text": "int number = 0X101Uf", "line": 1, "pos": 14},
    {"text": "int number = 0101f", "line": 1, "pos": 14},
    {"text": "float number=10.12fe10", "line": 1, "pos": 14},
    {"text": "float number=10.fU", "line": 1, "pos": 14},
    {"text": "float number=21.3E56E4654", "line": 1, "pos": 14},
    {"text": "float number=105e4d", "line": 1, "pos": 14},
    {"text": "float number=105flu", "line": 1, "pos": 14},
    {"text": "float number=105fu", "line": 1, "pos": 14},
    {"text": "float number=105eu", "line": 1, "pos": 14},
]


@pytest.mark.parametrize(
    "data", failed_tokens_tests, ids=[data["text"] for data in failed_tokens_tests]
)
def test_tokenizing_errors(data):
    text, line, pos = data.values()

    with pytest.raises(TokenError, match=f"({line}, {pos})"):
        Lexer(File("<file>", text)).check_tokens()
