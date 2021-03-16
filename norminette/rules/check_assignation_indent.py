from norminette.rules import Rule


operators = [
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
    "LESS_OR_EQUAL",
    "GREATER_OR_EQUAL",
    "EQUALS",
    "NOT_EQUAL",
    "ASSIGN",
    "SEMI_COLON",
    "DOT",
    "NOT",
    "MINUS",
    "PLUS",
    "MULT",
    "DIV",
    "MODULO",
    "LESS_THAN",
    "MORE_THAN",
    "PTR",
    "AND",
    "OR",
    "BWISE_XOR",
    "BWISE_OR",
    "BWISE_NOT",
    "BWISE_AND",
    "RIGHT_SHIFT",
    "LEFT_SHIFT",
]

nest_kw = ["RPARENTHESIS", "LPARENTHESIS", "NEWLINE"]


class CheckAssignationIndent(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsAssignation", "IsFuncPrototype", "IsFunctionCall"]

    def run(self, context):
        """
        Declared variables must be aligned using tabs with other variables on the same scope
        """
        i = 0
        expected = context.scope.indent
        if context.history[-1] == "IsAssignation":
            nest = expected + 1
        elif context.history[-1] == "IsFuncPrototype":
            nest = context.func_alignment
        else:
            nest = expected
        while context.check_token(i, ["SEMI_COLON"]) is False:
            if context.check_token(i, "NEWLINE") is True:
                if context.check_token(i - 1, operators) is True:
                    context.new_error("EOL_OPERATOR", context.peek_token(i))
                tmp = context.skip_ws(i + 1)
                if context.check_token(tmp, "COMMA"):
                    context.new_error("COMMA_START_LINE", context.peek_token(i))
                got = 0
                i += 1
                while context.check_token(i + got, "TAB") is True:
                    got += 1
                if context.check_token(i + got, ["LBRACKET", "RBRACKET", "LBRACE", "RBRACE"]):
                    nest -= 1
                if got > nest:
                    context.new_error("TOO_MANY_TAB", context.peek_token(i))
                    return True, i
                elif got < nest:
                    context.new_error("TOO_FEW_TAB", context.peek_token(i))
                    return True, i
                if context.check_token(i + got, ["LBRACKET", "RBRACKET", "LBRACE", "RBRACE"]):
                    nest += 1
            if context.check_token(i, "LPARENTHESIS") is True:
                nest += 1
            if context.check_token(i, "RPARENTHESIS") is True:
                nest -= 1
            i += 1
        return False, 0
