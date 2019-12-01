""" Dictionary that correlates lexeme with token """

keywords = {
    # C reserved keywords #
    'auto': "AUTO",
    'break': "BREAK",
    'case': "CASE",
    'char': "CHAR",
    'const': "CONST",
    'continue': "CONTINUE",
    'default': "DEFAULT",
    'do': "DO",
    'double': "DOUBLE",
    'else': "ELSE",
    'enum': "ENUM",
    'extern': "EXTERN",
    'float': "FLOAT",
    'for': "FOR",
    'goto': "GOTO",
    'if': "IF",
    'int': "INT",
    'long': "LONG",
    'register': "REGISTER",
    'return': "RETURN",
    'short': "SHORT",
    'signed': "SIGNED",
    'sizeof': "SIZEOF",
    'static': "STATIC",
    'struct': "STRUCT",
    'switch': "SWITCH",
    'typedef': "TYPEDEF",
    'union': "UNION",
    'unsigned': "UNSIGNED",
    'void': "VOID",
    'volatile': "VOLATILE",
    'while': "WHILE",
    # Preprocessor directives ##
    'define': "DEFINE",
    'error': "ERROR",
    'ifdef': "IFDEF",
    'ifndef': "IFNDEF",
    'include': "INCLUDE",
    'pragma': "PRAGMA",
    'undef': "UNDEF"
}

"""
__FILE__ ?add?
__LINE__ ?add?
__DATE__ ?add?
__TIME__ ?add?
__TIMESTAMP__ ?add?
"""

operators = {
    '>>=':  "OP_RIGHT_ASSIGN",
    '<<=':  "OP_LEFT_ASSIGN",
    '+=':   "OP_ADD_ASSIGN",
    '-=':   "OP_SUB_ASSIGN",
    '*=':   "OP_MUL_ASSIGN",
    '/=':   "OP_DIV_ASSIGN",
    '%=':   "OP_MOD_ASSIGN",
    '&=':   "OP_AND_ASSIGN",
    '^=':   "OP_XOR_ASSIGN",
    '|=':   "OP_OR_ASSIGN",
    '<=':   "OP_LE",
    '>=':   "OP_GE",
    '==':   "OP_EQ",
    '!=':   "OP_NE",
    '=':    "OP_ASSIGN",
    ';':    "OP_SEMI_COLON",
    ':':    "OP_COLON",
    ',':    "OP_COMMA",
    '.':    "OP_DOT",
    '!':    "OP_NOT",
    '-':    "OP_MINUS",
    '+':    "OP_PLUS",
    '*':    "OP_MULT",
    '/':    "OP_DIV",
    '%':    "OP_MODULO",
    '<':    "OP_LESS_THAN",
    '>':    "OP_MORE_THAN",
    '...':  "OP_ELLIPSIS",
    '++':   "OP_INC",
    '--':   "OP_DEC",
    '->':   "OP_PTR",
    '&&':   "OP_AND",
    '||':   "OP_OR",
    '^':    "OP_BWISE_XOR",
    '|':    "OP_BWISE_OR",
    '~':    "OP_BWISE_NOT",
    '&':    "OP_BWISE_AND",
    '>>':   "OP_RIGHT_SHIFT",
    '<<':   "OP_LEFT_SHIFT",
    '?':    "OP_TERN_CONDITION"
}

brackets = {
    '{':    "OPENING_BRACKET",
    '}':    "CLOSING_BRACKET",
    '(':    "OPENING_PARENTHESIS",
    ')':    "CLOSING_PARENTHESIS",
    '[':    "OPENING_SQUARE_BRACKET",
    ']':    "CLOSING_SQUARE_BRACKET"
}
