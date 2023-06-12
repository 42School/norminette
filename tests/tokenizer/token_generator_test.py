import pytest
import glob

from norminette.lexer import Lexer
from norminette.registry import Registry


registry = Registry()
test_files = glob.glob("tests/tokenizer/samples/ok/*.[ch]")

@pytest.mark.parametrize("file", test_files)
def test_rule_for_file(file):
    with open(file,'r') as test_file:
        file_to_lex = test_file.read()

    with open(f"{file.split('.')[0]}.tokens") as out_file:
        out_content = out_file.read()

    output = Lexer(file_to_lex).check_tokens()

    assert output == out_content
