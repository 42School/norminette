from norminette.rules import Rule

kw = [
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
    "STATIC",
    "STRUCT",
    "SWITCH",
    "TYPEDEF",
    "UNION",
    "UNSIGNED",
    "VOID",
    "VOLATILE",
    "WHILE",
]


class CheckExpressionStatement(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = [
            "IsExpressionStatement",
            "IsControlStatement",
            "IsFunctionCall",
            "IsAssignation",
        ]

    def run(self, context):
        """
        C keywords (return, break, continue...) must be followed by a space, with the
        exception of sizeof
        Return values in a function must be contained in parenthesis
        """
        i = 0
        parenthesis = False
        while context.check_token(i, ["SEMI_COLON", "NEWLINE"]) is False:
            if context.check_token(i, kw) is True:
                if context.check_token(i + 1, ["SPACE", "NEWLINE", "RPARENTHESIS"]) is False:
                    context.new_error("SPACE_AFTER_KW", context.peek_token(i))
                    return False, 0
            if context.check_token(i, "RETURN") is True:
                tmp = i + 1
                tmp = context.skip_ws(tmp)
                if context.check_token(tmp, "SEMI_COLON") is True:
                    return False, 0
                if (
                    context.check_token(tmp, "SEMI_COLON") is False
                    and context.check_token(tmp, "LPARENTHESIS") is False
                ):
                    context.new_error("RETURN_PARENTHESIS", context.peek_token(tmp))
                    return False, 0
                else:
                    tmp = context.skip_nest(tmp) + 1
                    if context.check_token(tmp, "SEMI_COLON") is False:
                        context.new_error("RETURN_PARENTHESIS", context.peek_token(tmp))
                    return False, 0
            i += 1
        return False, 0
