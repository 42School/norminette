from norminette.rules import Rule

class CheckManyInstructions(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = [
            "IsAssignation",
            "IsBlockEnd",
            "IsControlStatement",
            "IsExpressionStatement",
            "IsFuncDeclaration",
            "IsFuncPrototype",
            "IsUserDefinedType",
            "IsVarDeclaration",
            "IsFunctionCall",
        ]

    def run(self, context):
        """
        Each instruction must be separated by a newline
        """
        if context.peek_token(0).pos[1] > 1:
            context.new_error("TOO_MANY_INSTR", context.peek_token(0))
            return False, 0
        # if context.history[-1] in ["IsFuncDeclaration", "IsFuncPrototype", "IsControlStatement"]:
        #     return False, 0
        # i = 0
        # while i < context.tkn_scope:
        #     if context.check_token(i, SEPARATORS) is True:
        #         context.new_error("TOO_MANY_INSTR", context.peek_token(0))
        #         return False, 0
        #     i += 1
        return False, 0
