import pytest
import glob

from norminette.__main__ import colors
from norminette.lexer import Lexer, TokenError
from norminette.context import Context, CParsingError
from norminette.registry import Registry


registry = Registry()
test_files = glob.glob("tests/rules/samples/*.[ch]")


@pytest.mark.parametrize("file", test_files)
def test_rule_for_file(file, capsys):
    with open(file, "r") as test_file:
        file_to_lex = test_file.read()

    with open(f"{file.split('.')[0]}.out") as out_file:
        out_content = out_file.read()

    try:
        lexer = Lexer(file_to_lex)
        context = Context(file.split("/")[-1], lexer.get_tokens(), debug=2)
        registry.run(context, file_to_lex)
    except (TokenError, CParsingError) as e:
        captured = file + f": Error!\n\t{colors(e.msg, 'red')}" + '\n'
    else:
        captured = capsys.readouterr().out

    assert captured == out_content
