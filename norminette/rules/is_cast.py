from norminette.rules import Rule, Primary

types = [
    "CHAR",
    "DOUBLE",
    "ENUM",
    "FLOAT",
    "INT",
    "UNION",
    "VOID",
    "LONG",
    "SHORT",
    "SIGNED",
    "UNSIGNED",
    "STRUCT",
    "ENUM",
    "UNION",
    "CONST",
    "REGISTER",
    "STATIC",
    "VOLATILE",
]

op = [
    "MULT",
    "LPARENTHESIS",
    "RPARENTHESIS",
    "LBRACKET",
    "RBRACKET",
    "MINUS",
    "PLUS",
    "DIV",
    "PTR",
    "DOT",
]

ws = ["SPACE", "TAB", "NEWLINE"]


class IsCast(Rule, Primary, priority=15):
    def run(self, context):
        """
        Catches all casts instructions
        """
        i = 0
        i = context.skip_ws(i, nl=False)
        if context.check_token(i, "LPARENTHESIS") is True:
            ret, i = context.parenthesis_contain(i)
            if ret == "cast":
                while context.peek_token(i) and context.check_token(i, "SEMI_COLON") is False:
                    i += 1
                i += 1
                i = context.skip_ws(i, nl=False)
                i = context.eol(i)
                return True, i
        return False, 0
