from norminette.rules import Rule, Check


class CheckComment(Rule, Check):
    def run(self, context):
        """
        Comments are forbidden inside functions and in the middle of instructions.
        """
        i = context.skip_ws(0)

        tokens = []
        while context.peek_token(i) and not context.check_token(i, "NEWLINE"):
            token = context.peek_token(i)
            tokens.append(token)
            i += 1

        for index, token in enumerate(tokens):
            if token.type in ("COMMENT", "MULT_COMMENT"):
                if self.is_inside_a_function(context):
                    context.new_error("WRONG_SCOPE_COMMENT", token)
                if index == 0 or self.is_last_token(token, tokens[index+1:]):
                    continue
                context.new_error("COMMENT_ON_INSTR", token)

    def is_inside_a_function(self, context):
        if context.history[-2:] == ["IsFuncDeclaration", "IsBlockStart"]:
            return True
        if context.scope.__class__.__name__.lower() == "function":
            return True
        # Sometimes the context scope is a `ControlStructure` scope instead of
        # `Function` scope, so, to outsmart this bug, we need check manually
        # the `context.history`.
        last = None
        for index, record in enumerate(reversed(context.history)):
            if record == "IsFuncDeclaration" and last == "IsBlockStart":
                # Since the limited history API, we can't say if we're in a
                # nested function to reach the first enclosing function, so,
                # we'll consider that the user just declared a normal function
                # in global scope.
                stack = 1
                index -= 1  # Jumps to next record after `IsBlockStart`
                while index > 0 and stack > 0:
                    record = context.history[-index]
                    index -= 1
                    if record not in ("IsBlockStart", "IsBlockEnd"):
                        continue
                    stack = stack + (1, -1)[record == "IsBlockEnd"]
                return bool(stack)
            last = record
        return False

    def is_last_token(self, token, foward):
        expected = ("SPACE", "TAB")
        if token.type == "MULT_COMMENT":
            expected += ("COMMENT", "MULT_COMMENT")
        return all(it.type in ("SPACE", "TAB", "COMMENT", "MULT_COMMENT") for it in foward)
