from norminette.rules import Rule
from norminette.scope import GlobalScope


class CheckLineIndent(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = []

    def run(self, context):
        """
        Each new scope (function, control structure, struct/enum type declaration) adds a tab to the general indentation
        """
        expected = context.scope.indent
        if context.history[-1] in [
            "IsEmptyLine",
            "IsComment",
            "IsPreprocessorStatement",
            "IsVariableDeclaration",
        ]:
            return False, 0
        if (
            context.history[-1] != "IsPreprocessorStatement"
            and type(context.scope) is GlobalScope
            and context.scope.include_allowed is True
        ):
            context.scope.include_allowed = False
        got = 0
        while context.check_token(got, "TAB"):
            got += 1
        if context.check_token(got, ["LBRACE", "RBRACE"]) and expected > 0:
            if context.check_token(got, "RBRACE") is True:
                expected -= 1
            else:
                hist = context.history[: len(context.history) - 1]
                for item in hist[::-1]:
                    if (
                        item == "IsEmptyLine"
                        or item == "IsComment"
                        or item == "IsPreprocessorStatement"
                    ):
                        continue
                    if item not in [
                        "IsControlStatement",
                        "IsFuncDeclaration",
                        "IsUserDefinedType",
                    ]:
                        break
                    else:
                        expected -= 1
                    break
        if expected > got:
            context.new_error("TOO_FEW_TAB", context.peek_token(0))
            return False, got
        elif got > expected:
            context.new_error("TOO_MANY_TAB", context.peek_token(0))
            return False, got
        return False, 0
