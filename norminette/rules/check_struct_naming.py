from norminette.rules import Rule

types = [
    "STRUCT",
    "ENUM",
    "UNION",
]


class CheckStructNaming(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsUserDefinedType"]
        self.__i = 0

    def run(self, context):
        """
        Rewritten elsewhere
        """
        return False, 0
        self.__i += 1
        i = 0
        i = context.skip_ws(i)
        while context.check_token(i, types) is False:
            i += 1
        if context.check_token(i, "NEWLINE"):
            return False, 0
        def_type = context.peek_token(i).type
        i += 1
        i = context.skip_ws(i)
        if def_type == "STRUCT":
            if context.peek_token(i).value.startswith("s_") is False:
                context.new_error("STRUCT_TYPE_NAMING", context.peek_token(i))
        elif def_type == "ENUM":
            if context.peek_token(i).value.startswith("e_") is False:
                context.new_error("ENUM_TYPE_NAMING", context.peek_token(i))
        elif def_type == "UNION":
            if context.peek_token(i).value.startswith("u_") is False:
                context.new_error("UNION_TYPE_NAMING", context.peek_token(i))
        return False, i
