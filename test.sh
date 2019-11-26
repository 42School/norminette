echo "Running lexer unit test:"
python -m unittest discover tests/unit "*.py"
echo "Running lexer test on files:"
python -m unittest discover tests/files "*.py"
