import pytest
import glob

from norminette.file import File
from norminette.lexer import Lexer
from norminette.registry import Registry


registry = Registry()
test_files = glob.glob("tests/tokenizer/samples/ok/*.[ch]")


@pytest.mark.parametrize("file", test_files)
def test_rule_for_file(file):
    with open(f"{file.split('.')[0]}.tokens") as out_file:
        out_content = out_file.read()

    lexer = Lexer(File(file))

    output = ''
    tokens = list(lexer)
    if tokens:
        for token in tokens:
            output += str(token) + '\n' * int(token.type == "NEWLINE")
        if tokens[-1].type != "NEWLINE":
            output += "\n"

    assert output == out_content
