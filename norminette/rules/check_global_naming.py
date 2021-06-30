from norminette.rules import Rule

types = [
    "INT",
    "VOID",
    "CHAR",
    "LONG",
    "DOUBLE",
    "SHORT",
    "SIGNED",
    "UNSIGNED",
    "STATIC",
    "CONST",
    "IDENTIFIER",
    "ENUM",
    "STRUCT",
    "UNION",
    "VOLATILE",
    "EXTERN",
    "SPACE",
    "TAB",
]


class CheckGlobalNaming(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsVarDeclaration"]

    def run(self, context):
        """
        Global variable names must be preceded by g_
        """
        i = 0
        last_id = ""
        if context.scope.name != "GlobalScope":
            return False, 0
        i = context.skip_ws(i)
        _, i = context.check_type_specifier(i)
        while context.check_token(i, "IDENTIFIER") is False:
            i += 1
        if context.peek_token(i).value.startswith("g_") is False and context.peek_token(i).value != "environ":
            context.new_error("GLOBAL_VAR_NAMING", context.peek_token(i))
        return False, i
