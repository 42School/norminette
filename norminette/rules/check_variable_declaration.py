from rules import Rule
from scope import *

assigns = [
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
]

class CheckVariableDeclaration(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsVarDeclaration"]

    def run(self, context):
        i = 0
        static = False
        if context.scope.name == "Function":
            if context.history[-2] != "IsBlockStart" and context.history[-2] != "IsVarDeclaration":
                context.new_error("VAR_DECL_START_FUNC", context.peek_token(i))
            elif context.scope.vdeclarations_allowed == False:
                context.new_error("VAR_DECL_START_FUNC", context.peek_token(i))
            elif context.scope.vdeclarations_allowed == None:
                context.scope.vdeclarations_allowed = True
        elif context.scope.name == "GlobalScope" or context.scope.name == "UserDefinedType":
            pass
        else:
            context.new_error("WRONG_SCOPE_VAR", context.peek_token(i))
        while context.check_token(i, "SEMI_COLON") is False:
            if context.check_token(i, "STATIC") is True:
                static = True
            if context.check_token(i, assigns) is True and static == False:
                if context.scope.name == "GlobalScope":
                    i += 1
                    continue
                context.new_error("DECL_ASSIGN_LINE", context.peek_token(i))
            if context.check_token(i, "COMMA") is True:
                context.new_error("MULT_DECL_LINE", context.peek_token(i))
            i += 1
        return False, 0
