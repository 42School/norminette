from norminette.rules import Rule

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
        """
        Variables can be declared as global or in the scope of a function
        Only static variables, global variables, and constants can be initialised at declaration.
        Each variable must be declared on a separate line
        """
        i = 0
        static_or_const = False
        passed_assign = False
        if context.scope.name == "Function":
            context.scope.vars += 1
            if context.scope.vars > 5:
                context.new_error("TOO_MANY_VARS_FUNC", context.peek_token(i))
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
        tmp = 0
        ret, tmp = context.check_type_specifier(tmp)
        tmp -= 1
        identifier = False
        while context.check_token(tmp, ["SEMI_COLON"] + assigns) is False:
            if context.check_token(tmp, "IDENTIFIER"):
                identifier = True
            tmp += 1
        if identifier == False:
            context.new_error("IMPLICIT_VAR_TYPE", context.peek_token(0))
            return False
        while context.peek_token(i) and context.check_token(i, "SEMI_COLON") is False:
            if context.check_token(i, "LPARENTHESIS") is True:
                i = context.skip_nest(i)
            if context.check_token(i, "ASSIGN") is True:
                passed_assign = True
            if context.check_token(i, ["STATIC", "CONST"]) is True:
                static_or_const = True
            if context.check_token(i, assigns) is True and static_or_const == False:
                if context.scope.name == "GlobalScope":
                    i += 1
                    continue
                context.new_error("DECL_ASSIGN_LINE", context.peek_token(i))
            if context.check_token(i, "COMMA") is True and passed_assign == False:
                context.new_error("MULT_DECL_LINE", context.peek_token(i))
            i += 1
        return False, 0
