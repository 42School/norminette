import pytest
import glob

from norminette.lexer import Lexer
from norminette.context import Context
from norminette.registry import Registry


registry = Registry()
test_files = glob.glob("tests/rules/samples/*.[ch]")

@pytest.mark.parametrize("file", test_files)
def test_rule_for_file(file, capsys):
    with open(file,'r') as test_file:
        file_to_lex = test_file.read()

    with open(f"{file.split('.')[0]}.out") as out_file:
        out_content = out_file.read()

    lexer = Lexer(file_to_lex)
    context = Context(file.split("/")[-1], lexer.get_tokens(), debug=2)
    registry.run(context, file_to_lex)
    captured = capsys.readouterr()

    assert captured.out == out_content
