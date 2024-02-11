from typing import Dict, Any, List, Optional

import pytest

from norminette.file import File
from norminette.lexer import Lexer, Token as T
from norminette.lexer.dictionary import keywords, operators, brackets
from norminette.errors import Error as E, Highlight as H
from norminette.exceptions import UnexpectedEOF


def lexer_from_source(source: str, /) -> Lexer:
    file = File("<file>", source)
    return Lexer(file)


def dict_to_pytest_param(data: Dict[str, List[Any]]):
    params = []
    for id, values in data.items():
        param = pytest.param(*values, id=id)
        params.append(param)
    return params


@pytest.mark.parametrize("source, parameters, expected", dict_to_pytest_param({
    "No args": ["oi", {}, 'o'],
    "Empty source": ['', {}, None],
    "Collect over than source length": ["hello", {"collect": 10}, "hello"],
    "Collect with empty source": ['', {"collect": 3}, None],
    "Offset in empty source": ['', {"offset": 3}, None],
    "Offset": ["Hello", {"offset": 2}, 'l'],
    "Offset with collect": ["Hello, world!", {"offset": 7, "collect": 5}, "world"],
    "Offset over than source length with collect": ["Hello, world!", {"offset": 14, "collect": 3}, None],
    "Newline": ["\naa", {}, '\n'],
    "Escaped newline": ["\\\n", {}, '\\'],
}))
def test_lexer_raw_peek(source: str, parameters: Dict[str, Any], expected: Optional[str]):
    lexer = lexer_from_source(source)

    assert lexer.raw_peek(**parameters) == expected


@pytest.mark.parametrize("source, parameters, expected", dict_to_pytest_param({
    "Empty source": ['', {}, None],
    "One letter source": ['a', {}, 'a'],
    "Two letter source": ["ab", {}, 'a'],
    "Times with no source length": ['a', {"times": 2}, None],
    "Times with large source length": ["abc", {"times": 2}, "ab"],
    "Times with exact source length": ["abc", {"times": 3}, "abc"],
    "Tab": ["\t 2", {}, '\t'],
    "Tab with use_spaces": ["\t 2", {"use_spaces": True}, "    "],
    "Tab with use_spaces and times": ["\t 2", {"use_spaces": True, "times": 3}, "     2"],
    "Tab in second column with use_spaces and times": ["ch\t2", {"use_spaces": True, "times": 4}, "ch  2"],
    "Newline followed by a letter": ["\na", {}, '\n'],
    "Newline with times": ["\nab", {"times": 2}, "\na"],
    "Escaped newline in EOF": ["\\\n", {}, None],
    "Escaped newline in SOF": ["\\\nabc", {}, 'a'],
    "Escaped newline with times": ["a\\\nbc", {"times": 2}, "ab"],
    "Backslash followed by a escaped newline with times": ["\\\\\nab", {"times": 2}, r"\a"],
    "Escaped single quote without use_escape": [r"\'", {}, '\\'],
    "Escaped single quote with use_escape": [r"\'", {"use_escape": True}, r"\'"],
    "Escaped newline without use_escape": [r"\n", {}, '\\'],
    "Escaped newline with use_escape": [r"\'", {"use_escape": True}, r"\'"],
    "Twice escaped single quote with times but without use_escape": [r"\'\'", {"times": 4}, r"\'\'"],
    "String with escaped single quote twice with times but without use_escape": ["\"\\'\\'\"", {"times": 6},
                                                                                 "\"\\'\\'\""],
    "String with escaped single quote twice with times and use_escape": ["\"\\'\\'\"",
                                                                         {"times": 4, "use_escape": True},
                                                                         "\"\\'\\'\""],
    "Char containing newline with times and use_escape": [r"'\n'", {"times": 3, "use_escape": True}, r"'\n'"],
    "Use trigraph instead of backslash to escape single quote": ["??/'", {"use_escape": True}, r"\'"],
    "Use trigraph to escape newline with times": ["a??/\nb", {"times": 2, "use_escape": True}, r"ab"],
    "Multiples escaped newlines": ["\\\n\\\na\n", {}, 'a'],
    "Multiples escaped newlines with trigraphs": ["??/\n??/\na\n", {}, 'a'],
    "Bla": ["\\\na\n", {}, 'a'],
}))
def test_lexer_pop(source: str, parameters: Dict[str, Any], expected: Optional[str]):
    lexer = lexer_from_source(source)

    if expected is None:
        pytest.raises(UnexpectedEOF, lexer.pop, **parameters)
    else:
        assert lexer.pop(**parameters) == expected


@pytest.mark.parametrize("source, str_expected, errors", dict_to_pytest_param({
    "Unexpected EOF only quote": ['\'', "<CHAR_CONST='>", [
        E.from_name("UNEXPECTED_EOF_CHR", highlights=[H(lineno=1, column=1, length=1)])
    ]],
    "Unexpected EOF with quote and letter": ["'a", "<CHAR_CONST='a>", [
        E.from_name("UNEXPECTED_EOF_CHR", highlights=[H(lineno=1, column=1, length=2)]),
    ]],
    "Unexpected EOF with char as string": ["'Farofa ", "<CHAR_CONST='Farofa >", [
        E.from_name("UNEXPECTED_EOF_CHR", highlights=[H(lineno=1, column=1, length=len("'Farofa "))]),
    ]],
    "Unexpected EOL only quote": ["'\n", "<CHAR_CONST='>", [
        E.from_name("UNEXPECTED_EOL_CHR", highlights=[
            H(lineno=1, column=1, length=1),
            H(lineno=1, column=1 + len("'"), length=1, hint="Perhaps you forgot a single quote (')?"),
        ]),
    ]],
    "Unexpected EOL with quote and letter": ["'a\n", "<CHAR_CONST='a>", [
        E.from_name("UNEXPECTED_EOL_CHR", highlights=[
            H(lineno=1, column=1, length=2),
            H(lineno=1, column=1 + len("'a"), length=1, hint="Perhaps you forgot a single quote (')?"),
        ]),
    ]],
    "Unexpected EOL with char as string": ["'Astronauta\n", "<CHAR_CONST='Astronauta>", [
        E.from_name("UNEXPECTED_EOL_CHR", highlights=[
            H(lineno=1, column=1, length=len("'Astronauta")),
            H(lineno=1, column=1 + len("'Astronauta"), length=1, hint="Perhaps you forgot a single quote (')?"),
        ]),
    ]],
    "ASCII letter": ["'a'", "<CHAR_CONST='a'>", []],
    "ASCII number": ["'9'", "<CHAR_CONST='9'>", []],
    "Single quote escaped": [r"'\''", r"<CHAR_CONST='\''>", []],
    "Newline": [r"'\n'", r"<CHAR_CONST='\n'>", []],
    "Empty char": ["''", "<CHAR_CONST=''>", [
        E.from_name("EMPTY_CHAR", highlights=[H(lineno=1, column=1, length=2)])],
    ],
    "String quote": ['"a"', "None", []],
    "Int literal": ['1', "None", []],
    "Null": [r"'\0'", r"<CHAR_CONST='\0'>", []],
    "Hexadecimal char E9 (é)": [r"'\xE9'", R"<CHAR_CONST='\xE9'>", []],
    "Hexadecimal char without sequence": [r"'\x'", R"<CHAR_CONST='\x'>", [
        E.from_name("NO_HEX_DIGITS", level="Notice", highlights=[
            H(lineno=1, column=3, length=1),
        ]),
    ]],
    "Escape sequence that doesn't exists": [r"'\j'", r"<CHAR_CONST='\j'>", [
        E.from_name("UNKNOWN_ESCAPE", level="Notice", highlights=[
            H(lineno=1, column=3, length=1),
        ]),
    ]],
    "Char too long": ["'John Galt'", "<CHAR_CONST='John Galt'>", [
        E.from_name("CHAR_AS_STRING", highlights=[
            H(lineno=1, column=1, length=len("'John Galt'")),
            H(lineno=1, column=1, length=1,
              hint="Perhaps you want a string (double quote, \") instead of a char (single quote, ')?"),
        ])
    ]],
    "Char with L prefix": ["L'a'", "<CHAR_CONST=L'a'>", []],
    "Char escaped with L prefix": [r"L'\n'", r"<CHAR_CONST=L'\n'>", []],
    "Hex with one digit": [r"'\xA'", r"<CHAR_CONST='\xA'>", []],
    "Hex with two digits": [r"'\x3F'", r"<CHAR_CONST='\x3F'>", []],
}))
def test_lexer_parse_char_literal(source: str, str_expected: str, errors: List[E]):
    lexer = lexer_from_source(source)
    token = lexer.parse_char_literal()

    assert str(token) == str_expected
    assert repr(lexer.file.errors) == repr(errors)


@pytest.mark.parametrize("source, str_expected, errors", dict_to_pytest_param({
    "Empty string": ["\"\"", "<STRING=\"\">", []],
    "ASCII normal string": ["\"x+1=2, where x=1\"", "<STRING=\"x+1=2, where x=1\">", []],
    "Single quote string": ["'teste'", "None", []],
    "Unexpected EOF with empty string": ['\"', "<STRING=\">", [
        E.from_name("UNEXPECTED_EOF_STR", highlights=[
            H(lineno=1, column=1, length=1),
            H(lineno=1, column=2, length=1, hint="Perhaps you forgot a double quote (\")?"),
        ]),
    ]],
    "Unexpected EOF": ['\"asd', "<STRING=\"asd>", [
        E.from_name("UNEXPECTED_EOF_STR", highlights=[
            H(lineno=1, column=1, length=4),
            H(lineno=1, column=5, length=1, hint="Perhaps you forgot a double quote (\")?"),
        ]),
    ]],
    "String with escaped new line": ["\"first\\\n second\"", "<STRING=\"first second\">", []],
    "Basic string": ["\"Basic string\"", "<STRING=\"Basic string\">", []],
    "L basic string": ["L\"Basic string\"", "<STRING=L\"Basic string\">", []],
    "String with escaped quotes": ["\"Basic \\\"string\\\"\"", "<STRING=\"Basic \\\"string\\\"\">", []],
    "Multiples escapes and escaped quote": [r'"Escaped \\\"string\\\\\"\\"',
                                            r'<STRING="Escaped \\\"string\\\\\"\\">',
                                            []],
}))
def test_lexer_parse_string_literal(source: str, str_expected: str, errors: List[E]):
    lexer = lexer_from_source(source)
    token = lexer.parse_string_literal()

    assert str(token) == str_expected
    assert repr(lexer.file.errors) == repr(errors)


@pytest.mark.parametrize("source, str_expected", dict_to_pytest_param({
    "Empty comment": ["//", "<COMMENT=//>"],
    "Comment at EOF": ["// The sky is falling", "<COMMENT=// The sky is falling>"],
    "Comment at EOL": ["// The sky is falling\n", "<COMMENT=// The sky is falling>"],
    "Comment with escaped line in EOF": ["// The sky is falling\\", r"<COMMENT=// The sky is falling\>"],
    "Comment with escaped line in EOF using trigraph": [r"// The sky is falling??/",
                                                        r"<COMMENT=// The sky is falling\>"],
    "Comment with escaped line": ["// The sky is falling\\\n!", "<COMMENT=// The sky is falling!>"],
    "Comment with escaped line using trigraph": ["// The sky is falling??/\n!", "<COMMENT=// The sky is falling!>"],
}))
def test_lexer_parse_line_comment(source: str, str_expected: str):
    lexer = lexer_from_source(source)
    token = lexer.parse_line_comment()

    assert str(token) == str_expected
    assert lexer.file.errors.status == "OK"


@pytest.mark.parametrize("source, str_expected, errors", dict_to_pytest_param({
    "Multi-line comment in single line at EOF": ["/* The sky is falling*/",
                                                 "<MULT_COMMENT=/* The sky is falling*/>", []],
    "Multi-line comment in multiples lines at EOF": ["/*\na\nb\n\n\n*/", "<MULT_COMMENT=/*\na\nb\n\n\n*/>", []],
    "Multi-line comment with escaped line": ["/*\\\na*/", "<MULT_COMMENT=/*a*/>", []],
    "Multi-line comment with escaped line using trigraph": ["/*??/\na*/", "<MULT_COMMENT=/*a*/>", []],
    "Multi-line comment not terminated with escaped line before EOF": ["/*\\\n", "<MULT_COMMENT=/*>", [
        E.from_name("UNEXPECTED_EOF_MC", highlights=[
            H(lineno=1, column=1, length=len("/*")),
        ]),
    ]],
    "Multi-line comment not terminated": ["/* uepaaa\ne agora??", "<MULT_COMMENT=/* uepaaa\ne agora??>", [
        E.from_name("UNEXPECTED_EOF_MC", highlights=[
            H(lineno=1, column=1, length=len("/* uepaaa\ne agora??")),
        ]),
    ]],
    "Multi-line comment not terminate ending with a backslash": ["/*\\", r"<MULT_COMMENT=/*\>", [
        E.from_name("UNEXPECTED_EOF_MC", highlights=[
            H(lineno=1, column=1, length=len("/*\\")),
        ]),
    ]],
    "Comment (not multi-line)": ["// hey, i'm not a multi-line comment", "None", []],
    "Space before a multi-line comment": [" /* */", "None", []],
}))
def test_lexer_parse_multi_line_comment(source: str, str_expected: str, errors: List[E]):
    lexer = lexer_from_source(source)
    token = lexer.parse_multi_line_comment()

    assert str(token) == str_expected
    assert repr(lexer.file.errors) == repr(errors)


@pytest.mark.parametrize("source, str_expected, errors", dict_to_pytest_param({
    "Decimal integer": ["1234567890", "<CONSTANT=1234567890>", []],
    "Decimal integer with UL as suffix": ["1234567890UL", "<CONSTANT=1234567890UL>", []],
    "Decimal integer with bad suffix": ["1234567890ABC", "<CONSTANT=1234567890ABC>", [
        E.from_name("INVALID_SUFFIX", highlights=[
            H(lineno=1, column=11, length=len("ABC")),
        ]),
    ]],
    "Binary integer": ["0b1101011", "<CONSTANT=0b1101011>", []],
    "Binary integer with U as suffix": ["0b000001U", "<CONSTANT=0b000001U>", []],
    "Binary integer with bad digits": ["0b1210491011", "<CONSTANT=0b1210491011>", [
        E.from_name("INVALID_BIN_INT", highlights=[
            H(lineno=1, column=4, length=1, hint=None),  # 2
            H(lineno=1, column=7, length=1, hint=None),  # 4
            H(lineno=1, column=8, length=1, hint=None),  # 9
        ]),
    ]],
    "Octal integer": ["01234567123", "<CONSTANT=01234567123>", []],
    "Octal integer with U as suffix": ["0123u", "<CONSTANT=0123u>", []],
    "Octal integer with bad digits": ["00072189", "<CONSTANT=00072189>", [
        E.from_name("INVALID_OCT_INT", highlights=[
            H(lineno=1, column=7, length=1, hint=None),  # 8
            H(lineno=1, column=8, length=1, hint=None),  # 9
        ]),
    ]],
    "Octal integer with bad suffix with dots": ["000123u.23", "<CONSTANT=000123u.23>", [
        E.from_name("INVALID_SUFFIX", highlights=[
            H(lineno=1, column=len("000123") + 1, length=len("u.23")),
        ]),
    ]],
    "Integer with u suffix": ["123u", "<CONSTANT=123u>", []],
    "Integer with U suffix": ["123U", "<CONSTANT=123U>", []],
    "Integer with uz suffix": ["123uz", "<CONSTANT=123uz>", []],
    "Integer with UZ suffix": ["123UZ", "<CONSTANT=123UZ>", []],
    "Integer with z suffix": ["123z", "<CONSTANT=123z>", []],
    "Integer with Z suffix": ["123Z", "<CONSTANT=123Z>", []],
    "Integer with ul suffix": ["123ul", "<CONSTANT=123ul>", []],
    "Integer with UL suffix": ["123UL", "<CONSTANT=123UL>", []],
    "Integer with ull suffix": ["123ull", "<CONSTANT=123ull>", []],
    "Integer with ULL suffix": ["123ULL", "<CONSTANT=123ULL>", []],
    "Integer with ll suffix": ["9000000000ll", "<CONSTANT=9000000000ll>", []],
    "Integer with LL suffix": ["9000000000LL", "<CONSTANT=9000000000LL>", []],
    "Integer with bad suffix": ["10Uu", "<CONSTANT=10Uu>", [
        E.from_name("INVALID_SUFFIX", highlights=[
            H(lineno=1, column=1, length=len("10")),
        ]),
    ]],
}))
def test_lexer_parse_integer_literal(source: str, str_expected: str, errors: List[E]):
    lexer = lexer_from_source(source)
    token = lexer.parse_integer_literal()

    assert str(token) == str_expected
    assert repr(lexer.file.errors) == repr(errors)


@pytest.mark.parametrize("source, str_expected, errors", dict_to_pytest_param({
    "Integer": ["1234567890", "None", []],
    "Integer with exponent-part": ["1e2", "<CONSTANT=1e2>", []],
    "Integer with exponent-part and f as suffix": ["1e2f", "<CONSTANT=1e2f>", []],
    "Integer with bad exponent-part": ["1eeee2xf", "<CONSTANT=1eeee2xf>", [
        E.from_name("BAD_EXPONENT", highlights=[H(lineno=1, column=2, length=7)]),
    ]],
    "Exponent with sign": ["1e+3", "<CONSTANT=1e+3>", []],
    "": ["45e++ai", "None", []],
    "": ["e42", "None", []],
    "": ["0x1uLl;", "None", []],
    "": [".0e4x;", "None", []],
    "": ["10ul;", "None", []],
    "": ["10lul;", "None", []],
    "": ["0x1uLl;", "None", []],
    "": ["0x1ULl;", "None", []],
    "": ["0x1lL;", "None", []],
    "": ["0x1Ll;", "None", []],
    "": ["0x1UlL;", "None", []],
    "Integer with bad suffix": ["10uu", "None", []],
    "": ["10Uu", "None", []],
    "": ["10UU", "None", []],
    "": ["0b0101e", "None", []],
    "": ["0b0101f", "None", []],
    "": ["0b0X101f", "None", []],
    "": ["0X101Uf", "None", []],
    "": ["0101f", "None", []],
    "": ["10.12fe10", "None", []],
    "": ["10.fU", "None", []],
    "": ["21.3E56E4654", "None", []],
    "": ["105e4d", "None", []],
    "": ["105flu", "None", []],
    "": ["105fu", "None", []],
    "": ["105eu", "None", []],
}))
def test_lexer_parse_float_literal(source: str, str_expected: str, errors: List[E]):
    lexer = lexer_from_source(source)
    token = lexer.parse_float_literal()

    assert str(token) == str_expected
    assert repr(lexer.file.errors) == repr(errors)


@pytest.mark.parametrize("source, str_expected", dict_to_pytest_param({
    "Identifier starting with an integer": ["42_hello", "None"],
    "Identifier starting with an underscore": ["_hello", "<IDENTIFIER=_hello>"],
    "ft_printf identifier": ["ft_printf", "<IDENTIFIER=ft_printf>"],
    "Identifier with just underscore": ['_', "<IDENTIFIER=_>"],
    "Identifier with just one letter": ['a', "<IDENTIFIER=a>"],
    "Identifier with uppercase letters": ["EGGS", "<IDENTIFIER=EGGS>"],
    "Identifier with mixedcase letters": ["AbCd", "<IDENTIFIER=AbCd>"],
    "Identifier with lowercase letters": ["duck", "<IDENTIFIER=duck>"],
    "Identifier with an hyphen": ["clojure-is-cool", "<IDENTIFIER=clojure>"],
    "Identifier with integers, letters and underscores": ["ascii_2_bigint128", "<IDENTIFIER=ascii_2_bigint128>"],
    "String starting with an letter": ["L\"ola\"", "<IDENTIFIER=L>"],
    "Char starting with an letter": ["L'1'", "<IDENTIFIER=L>"],
}))
def test_lexer_parse_identifier(source: str, str_expected: str):
    lexer = lexer_from_source(source)
    token = lexer.parse_identifier()

    assert str(token) == str_expected
    assert lexer.file.errors.status == "OK"


@pytest.mark.parametrize("keyword", keywords.keys())
def test_lexer_parse_identifier_keyword_only(keyword: str):
    lexer = lexer_from_source(keyword)
    token = lexer.parse_identifier()

    assert str(token) == f"<{keyword.upper()}>"
    assert lexer.file.errors.status == "OK"


@pytest.mark.parametrize("operator, token_type", operators.items())
def test_lexer_parse_operator(operator: str, token_type: str):
    lexer = lexer_from_source(operator)
    token = lexer.parse_operator()

    assert str(token) == f"<{token_type}>"
    assert lexer.file.errors.status == "OK"


@pytest.mark.parametrize("bracket, token_type", brackets.items())
def test_lexer_parse_brackets(bracket: str, token_type: str):
    lexer = lexer_from_source(bracket)
    token = lexer.parse_brackets()

    assert str(token) == f"<{token_type}>"
    assert lexer.file.errors.status == "OK"


@pytest.mark.parametrize("source, expected_tokens", dict_to_pytest_param({
    "Empty source": ['', []],
    "Just space source": ["   ", [
        T("SPACE", (1, 1)),
        T("SPACE", (1, 2)),
        T("SPACE", (1, 3)),
    ]],
    "Identifier followed by a comment": ["test//comment", [
        T("IDENTIFIER", (1, 1), "test"),
        T("COMMENT", (1, 5), "//comment"),
    ]],
    "Main function prototype with void": ["int\tmain(void);", [
        T("INT", (1, 1)),
        T("TAB", (1, 4)),
        T("IDENTIFIER", (1, 5), value="main"),
        T("LPARENTHESIS", (1, 9)),
        T("VOID", (1, 10)),
        T("RPARENTHESIS", (1, 14)),
        T("SEMI_COLON", (1, 15)),
    ]],
    # Checks if `identifier` is bellow to `char` and `string`
    "Wide char/string followed by identifier": ["L'a' L\"bcd\" name", [
        T("CHAR_CONST", (1, 1), value="L'a'"),
        T("SPACE", (1, 5)),
        T("STRING", (1, 6), value="L\"bcd\""),
        T("SPACE", (1, 12)),
        T("IDENTIFIER", (1, 13), value="name"),
    ]],
    "Integer": ["42", [T("CONSTANT", (1, 1), value="42")]],
    "Integer with plus sign": ["+42", [
        T("PLUS", (1, 1)),
        T("CONSTANT", (1, 2), value="42"),
    ]],
    "Integer with minus sign": ["-42", [
        T("MINUS", (1, 1)),
        T("CONSTANT", (1, 2), value="42"),
    ]],
    "Integer with double sign": ["+-42", [
        T("PLUS", (1, 1)),
        T("MINUS", (1, 2)),
        T("CONSTANT", (1, 3), value="42"),
    ]],
    "Float": ["4.2", [T("CONSTANT", (1, 1), value="4.2")]],
    "Float without integer part": [".42", [T("CONSTANT", (1, 1), value=".42")]],
    "Float exponential": ["4e2", [T("CONSTANT", (1, 1), value="4e2")]],
    "Float with exponential in fractional part without integer": [".4e2", [T("CONSTANT", (1, 1), value=".4e2")]],
    "Float exponential with suffix": ["4e2f", [T("CONSTANT", (1, 1), value="4e2f")]],
    "Float exponential in fractional part with suffix": [".4e2f", [T("CONSTANT", (1, 1), value=".4e2f")]],
    "Octal": ["042", [T("CONSTANT", (1, 1), value="042")]],
    "Hexadecimal": ["0x42", [T("CONSTANT", (1, 1), value="0x42")]],
    "Negative hexadecimal": ["-0x4e2", [
        T("MINUS", (1, 1)),
        T("CONSTANT", (1, 2), value="0x4e2"),
    ]],
    "Integer with l as suffix": ["42l", [T("CONSTANT", (1, 1), value="42l")]],
    "Integer with ul as suffix": ["42ul", [T("CONSTANT", (1, 1), value="42ul")]],
    "Integer with ll as suffix": ["42ll", [T("CONSTANT", (1, 1), value="42ll")]],
    "Integer with ull as suffix": ["42ull", [T("CONSTANT", (1, 1), value="42ull")]],
    "Integer with u suffix": ["42u", [T("CONSTANT", (1, 1), value="42u")]],
    "Multiples signs": ["-+-+-+-+-+-+-+-0Xe4Ae2", [
        T("MINUS", (1, 1)),
        T("PLUS", (1, 2)),
        T("MINUS", (1, 3)),
        T("PLUS", (1, 4)),
        T("MINUS", (1, 5)),
        T("PLUS", (1, 6)),
        T("MINUS", (1, 7)),
        T("PLUS", (1, 8)),
        T("MINUS", (1, 9)),
        T("PLUS", (1, 10)),
        T("MINUS", (1, 11)),
        T("PLUS", (1, 12)),
        T("MINUS", (1, 13)),
        T("PLUS", (1, 14)),
        T("MINUS", (1, 15)),
        T("CONSTANT", (1, 16), value="0Xe4Ae2"),
    ]],
    "Member expression with left part": [".e42", [
        T("DOT", (1, 1)),
        T("IDENTIFIER", (1, 2), value="e42")
    ]],
    "Multiples dots in float": ["4.4.4", [T("CONSTANT", (1, 1), value="4.4.4")]],
    "Multiples exponents": ["4e4e4", [T("CONSTANT", (1, 1), value="4e4e4")]],
    "Bad suffix 1": ["4x4x4", [T("CONSTANT", (1, 1), value="4x4x4")]],
    "Bad suffix 2": ["42uul", [T("CONSTANT", (1, 1), value="42uul")]],
    "Bad suffix 3": ["42Lllu", [T("CONSTANT", (1, 1), value="42Lllu")]],
    "Bad suffix 4": ["42lul", [T("CONSTANT", (1, 1), value="42lul")]],
    "Bad exponent": [".42e", [T("CONSTANT", (1, 1), ".42e")]],
    "Escaped newline followed by an identifier": ["\\\nhello;", [
        T("IDENTIFIER", (2, 1), value="hello"),
        T("SEMI_COLON", (2, 6)),
    ]]
    # TODO Add to check prepoc tokens
}))
def test_lexer_tokens(source: str, expected_tokens: List[T]):
    lexer = lexer_from_source(source)
    tokens = list(lexer)

    assert tokens == expected_tokens
