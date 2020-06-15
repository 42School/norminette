echo "Running lexer unit test:"
python3.7 -m unittest discover tests/lexer/unit-tests/ "*.py"
echo "Running lexer test on files:"
python3.7 -m  tests.lexer.files.file_token_test
python3.7 -m tests.lexer.errors.tester
python3.7 -m tests.rules.rule_tester
