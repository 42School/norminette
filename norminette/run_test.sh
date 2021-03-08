#!/bin/env sh

python3 --version
set -ex

echo "Running lexer unit test:"
python3 -m unittest discover tests/lexer/unit-tests/ "*.py"
echo "Running lexer test on files:"
python3 -m  tests.lexer.files.file_token_test
python3 -m tests.lexer.errors.tester
python3 -m tests.rules.rule_tester
