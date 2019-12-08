echo "Running lexer unit test:"
python -m unittest discover tests/lexer/unit-tests/ "*.py"
echo "Running lexer test on files:"
python -m  tests.lexer.files.file_token_test
python -m tests.lexer.errors.tester
