errors = {
    "SPC_INSTEAD_TAB": "Spaces at beginning of line",
    "CONSECUTIVE_SPC": "Two or more consecutives spaces",
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
    "TOO_FEW_TAB": "Missing tabs for indent level",
    "TOO_MANY_TAB": "Extra tabs for indent level",
    "SPACE_REPLACE_TAB": "Found space when expecting tab",
    1021: "function has more than 25 lines",
    "SPACE_EMPTY_LINE": "Space on empty line",
    "SPC_BEFORE_NL": "Space before newline",
    1024: "Too many instructions on a single line",
    "PREPROC_UKN_STATEMENT": "Unrecognized preprocessor statement",
    "PREPROC_START_LINE": "Preprocessor statement not at the beginning of the\
 line",
    "PREPROC_CONSTANT": "Preprocessor statement must only contain constant\
 defines",
    "PREPROC_EXPECTED_EOL": "Expected EOL after preprocessor statement",
    "PREPROC_BAD_INDENT": "Bad preprocessor indentation",
    "USER_DEFINED_TYPEDEF": "User defined typedef must start with t_",
    "STRUCT_TYPE_NAMING": "Structure name must start with s_",
    "ENUM_TYPE_NAMING": "Enum name must start with e_",
    "UNION_TYPE_NAMING": "Union name must start with u_",
    "GLOBAL_VAR_NAMING": "Global variable must start with g_",
    "EOL_OPERATOR": "Logic operator at the end of line",
    "EMPTY_LINE_FUNCTION": "Empty line in function",
    "EMPTY_LINE_FILE_START": "Empty line at start of file",
    "EMPTY_LINE_FUNCTION": "Empty line in function",
    "EMPTY_LINE_EOF": "Empty line at end of file",
    "WRONG_SCOPE_VAR": "Variable declared in incorrect scope",
    "VAR_DECL_START_FUNC": "Variable declaration not at start of function",
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
        self.prefix = f"\t{self.errno} " + self.error_pos
        self.error_msg = f"{errors.get(self.errno, 'ERROR NOT FOUND')}"

    def __str__(self):
        return self.prefix + self.error_msg
