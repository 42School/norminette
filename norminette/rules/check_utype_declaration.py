from rules import Rule
from lexer import Lexer, TokenError
import math
from exceptions import CParsingError

types = [
    "STRUCT",
    "ENUM",
    "UNION",
    "INT",
    "VOID",
    "CHAR",
    "UNSIGNED",
    "CONST",
    "DOUBLE",
    "LONG",
    "SHORT",
    "STATIC",
    "IDENTIFIER",
    "SPACE",
    "TAB"
]

utypes = [
    "STRUCT",
    "ENUM",
    "UNION"
]

class CheckUtypeDeclaration(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsUserDefinedType"]

    def run(self, context):
        i = 0
        i = context.skip_ws(i)
        tkns = context.tokens
        is_td = False
        utype = None
        contain_full_def = False
        ids = []
        while context.check_token(i, ['SEMI_COLON']) is False and i < len(context.tokens):
            if context.check_token(i, ['SPACE', 'TAB']):
                pass
            if context.check_token(i, utypes) is True:
                utype = context.peek_token(i)
            if context.check_token(i, "TYPEDEF") is True:
                is_td = True
            if context.check_token(i, "IDENTIFIER") is True:
                ids.append((context.peek_token(i), i))
            if context.check_token(i, 'LBRACE') is True:
                contain_full_def = True
                i = context.skip_nest(i)
            i += 1
        check = -1
        if contain_full_def == False and is_td == False and len(ids) > 1:
            check = -2
        else:
            check = -1
        if len(ids) == 0:
            return False, 0
        name = ids[check][0]
        loc = ids[check][1]
        if is_td == True:
            if ids[check][0].value.startswith('t_') is False:
                context.new_error("USER_DEFINED_TYPEDEF", context.peek_token(loc))
            if utype is not None:
                if len(ids) > 1:
                    name = ids[check - 1][0]
                else:
                    pass
                    #raise CParsingError(f"{context.filename}: Could not parse structure line {context.peek_token(0).pos[0]}")
            loc = ids[check][1]
        if utype is not None and utype.type == "STRUCT" and name.value.startswith('s_') is False:
            context.new_error("STRUCT_TYPE_NAMING", context.peek_token(loc))
        if utype is not None and utype.type == "UNION" and name.value.startswith('u_') is False:
            context.new_error("UNION_TYPE_NAMING", context.peek_token(loc))
        if utype is not None and utype.type == "ENUM" and name.value.startswith('e_') is False:
            context.new_error("ENUM_TYPE_NAMING", context.peek_token(loc))
        if is_td or (is_td == False and contain_full_def == False):
            tmp = ids[-1][1] - 1
            while (context.check_token(tmp, "TAB")) is True and tmp > 0:
                tmp -= 1
            if context.check_token(tmp, "SPACE") is True:
                context.new_error("SPACE_REPLACE_TAB", context.peek_token(tmp))
            while tmp > 0:
                if context.check_token(tmp, "RBRACE") is True:
                    while context.check_token(tmp, "LBRACE") is False and tmp > 0:
                        tmp -= 1
                    continue
                if context.check_token(tmp, "TAB") is True:
                    context.new_error("SPACE_REPLACE_TAB", context.peek_token(tmp))
                tmp -= 1
        if contain_full_def == False:
            i = 0
            current_indent = ids[-1][0].pos[1]
            if context.scope.vars_alignment == 0:
                context.scope.vars_alignment = current_indent
            elif context.scope.vars_alignment != current_indent:
                context.new_error("MISALIGNED_VAR_DECL", context.peek_token(0))
                return True, i
            return False, 0














            current_indent = context.scope.indent
            while context.check_token(i, "SEMI_COLON") is False:
                if context.check_token(i, 'IDENTIFIER'):
                    if context.peek_token(i).value == ids[-1][0]:
                        if context.scope.vars_alignment == 0:
                            context.scope.vars_alignment = current_indent
                        elif current_indent != context.scope.vars_alignment:
                            context.new_error("MISALIGNED_VAR_DECL", context.peek_token(i))
                            return True, i
                        return False, 0
                    current_indent += math.floor((len(context.peek_token(i).value)) / 4)
                elif context.check_token(i, ["STRUCT", "ENUM", "UNION"]):
                    current_indent += 2
                elif context.check_token(i, "TAB"):
                    current_indent += 1
                i += 1
        return False, 0
