from rules import Rule
from scope import *
import math


keywords = [
    # C reserved keywords #
    "AUTO",
    "BREAK",
    "CASE",
    "CHAR",
    "CONST",
    "CONTINUE",
    "DEFAULT",
    "DO",
    "DOUBLE",
    "ELSE",
    "ENUM",
    "EXTERN",
    "FLOAT",
    "FOR",
    "GOTO",
    "IF",
    "INT",
    "LONG",
    "REGISTER",
    "RETURN",
    "SHORT",
    "SIGNED",
    "SIZEOF",
    "STATIC",
    "STRUCT",
    "SWITCH",
    "TYPEDEF",
    "UNION",
    "UNSIGNED",
    "VOID",
    "VOLATILE",
    "WHILE", 
    "IDENTIFIER"
]
assigns_or_eol = [
    "RIGHT_ASSIGN",
    "LEFT_ASSIGN",
    "ADD_ASSIGN",
    "SUB_ASSIGN",
    "MUL_ASSIGN",
    "DIV_ASSIGN",
    "MOD_ASSIGN",
    "AND_ASSIGN",
    "XOR_ASSIGN",
    "OR_ASSIGN",
    "ASSIGN",
    "SEMI_COLON",
    "NEWLINE"
]

class CheckVariableIndent(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsVarDeclaration"]


    def check_tabs(self, context):
        i = 0
        current_indent = context.scope.indent
        type_identifier_nb = -1
        has_tab = False
        line_start = True
        id_length = 0
        buffer_len = 0
        while context.check_token(i, assigns_or_eol) is False:
            if context.check_token(i, keywords) is True:
                type_identifier_nb += 1
            i += 1
        i = 0
        while context.check_token(i, assigns_or_eol) is False:
            if context.check_token(i, "LBRACKET") is True:
                while context.check_token(i, "RBRACKET") is False:
                    if context.check_token(i, "IDENTIFIER") is True:
                        context.new_error("VLA_FORBIDDEN", context.peek_token(i))
                        return True, i
                    i += 1
            if context.check_token(i, keywords) is True and type_identifier_nb > 0:
                line_start = False
                type_identifier_nb -= 1
                if context.peek_token(i).length == 0:
                    id_length = len(str(context.peek_token(i))) - 2
                else:
                    id_length = context.peek_token(i).length
                current_indent += math.floor((id_length + buffer_len) / 4)
                buffer_len = 0
            elif context.check_token(i, "SPACE") is True and type_identifier_nb > 0:
                buffer_len += 1

            elif context.check_token(i, "SPACE") is True and type_identifier_nb == 0:
                context.new_error("SPACE_REPLACE_TAB", context.peek_token(i))
                return True, i
            elif context.check_token(i, "TAB") is True and type_identifier_nb == 0:
                has_tab += 1
                current_indent += 1
                type_identifier_nb -= 1
            elif context.check_token(i, "TAB") and type_identifier_nb > 0 and \
                line_start == False:
                context.new_error("TAB_REPLACE_SPACE", context.peek_token(i))
            i += 1
        return False, 0

    def run(self, context):
        i = 0
        identifier = None
        self.check_tabs(context)
        while context.check_token(i, "SEMI_COLON") is False:
            if context.check_token(i, "IDENTIFIER") is True:
                while context.check_token(i - 1, ["MULT", "BWISE_AND"]) is True \
                and context.is_operator(i - 1) is False:
                    i -= 1
                identifier = context.peek_token(i)
            i += 1
        if context.scope.vars_alignment == 0:
            context.scope.vars_alignment = identifier.pos[1]
        elif context.scope.vars_alignment != identifier.pos[1]:
            context.new_error("MISALIGNED_VAR_DECL", context.peek_token(i))
            return True, i
        return False, 0




