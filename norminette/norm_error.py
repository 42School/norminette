errors = {
    1000: "spaces at beginning of line",
    1001: "two or more consecutives spaces",
    1002: "space after tab",
    1003: "missing space before operator",
    1004: "missing space after operator",
    1005: "extra space before operator",
    1006: "extra space after operator",
    1007: "space after pointer",
    1008: "bad spacing before pointer",
    1010: "space before function name",
    1011: "extra tabs before function name",
    1012: "missing tab before function name",
    1013: "braces should be on their own line",
    1014: "line too long",
    1015: "missing 'void' keyword",
    1016: "missing type qualifier or identifier in function arguments",
    1017: "function has more than four arguments",
    1018: "user defined identifiers should contain only lowercase characters, \
digits or '_'",
    1019: "missing tabs for indent level",
    1020: "extra tabs for indent level",
    1021: "function has more than 25 lines",
    1022: "space or tab on empty line",
    1023: "space before newline",
    "PREPROC_UKN_STATEMENT": "Unrecognized preprocessor statement",
    "PREPROC_START_LINE": "Preprocessor statement not at the beginning of the line",
    "PREPROC_CONSTANT": "Preprocessor statement must only contain constant defines",
    "PREPROC_EXPECTED_EOL": "Expected EOL after preprocessor statement",
    "PREPROC_BAD_INDENT": "Bad preprocessor indentation",
    # This is a dummy rule
    9999: "Consecutive newlines"
}


class NormError:
    def __init__(self, errno, line, col=None):
        self.errno = errno
        self.line = line
        self.col = col
        if col is not None:
            self.error_pos = f"(line: {self.line}, col: {self.col}):\t"
        else:
            self.error_pos = f"(line: {self.line}):\t "
        self.prefix = f"\tE{self.errno} " + self.error_pos
        self.error_msg = f"{errors.get(self.errno, 'ERROR NOT FOUND')}"

    def __str__(self):
        return self.prefix + self.error_msg
