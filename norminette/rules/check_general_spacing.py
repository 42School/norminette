from norminette.rules import Rule, Check


class CheckGeneralSpacing(Rule, Check):
    depends_on = (
        "IsDeclaration",
        "IsControlStatement",
        "IsExpressionStatement",
        "IsAssignation",
        "IsFunctionCall",
    )

    def run(self, context):
        """
        Checks for tab/space consistency
        """
        if context.scope.name == "UserDefinedType":
            return False, 0
        i = context.skip_ws(0)
        while i < context.tkn_scope:
            if context.check_token(i, "TAB") is True:
                context.new_error("TAB_INSTEAD_SPC", context.peek_token(i))
                break
            if context.check_token(i, ["NEWLINE", "ESCAPED_NEWLINE"]) is True:
                i = context.skip_ws(i + 1, nl=True)
            i += 1
        return False, 0
