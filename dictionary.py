""" Dictionary that correlates lexeme with token """

keywords = {
## C reserved keywords ##
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
## Preprocessor directives ##
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
    'assign' : {
        '>>=':  "RIGHT_ASSIGN",
        '<<=':  "LEFT_ASSIGN",
        '+=':   "ADD_ASSIGN",
        '-=':   "SUB_ASSIGN",
        '*=':   "MUL_ASSIGN",
        '/=':   "DIV_ASSIGN",
        '%=':   "MOD_ASSIGN",
        '&=':   "AND_ASSIGN",
        '^=':   "XOR_ASSIGN",
        '|=':   "OR_ASSIGN",
        '=':    "ASSIGN",
    },
    'regular' : {
        '...':  "ELLIPSIS",
        ';':    "SEMI_COLON",
        ':':    "COLON",
        ',':    "COMMA",
        '.':    "DOT",
        '&':    "AND",
        '!':    "NOT",
        '~':    "TILDE",
        '-':    "MINUS",
        '+':    "PLUS",
        '*':    "MULT",
        '/':    "DIV",
        '%':    "MODULO",
        '<':    "LESS THAN",
        '>':    "MORE THAN",
        '>>':   "RIGHT_SHIFT",
        '<<':   "LEFT_SHIFT",
        '++':   "INC",
        '--':   "DEC",
        '->':   "PTR_OP",
        '&&':   "AND_OP",
        '||':   "OR_OP",
        '<=':   "LE_OP",
        '>=':   "GE_OP",
        '==':   "EQ_OP",
        '!=':   "NE_OP",
        '^':    "XOR",
        '|':    "OR",
        '?':    "?"
    }
}

brackets = {
    '{':    "OPENING_BRACKET",
    '}':    "CLOSING_BRACKET",
    '(':    "OPENING_PARENTHESIS",
    ')':    "CLOSING_PARENTHESIS",
    '[':    "OPENING_SQUARE_BRACKET",
    ']':    "CLOSING_SQUARE_BRACKET" }
