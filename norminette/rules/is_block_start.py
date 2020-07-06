from lexer import Token
from rules import PrimaryRule
from scope import *
from context import (
                    Function,
                    UserDefinedType,
                    VariableAssignation,
                    ControlStructure)


class IsBlockStart(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 10
        self.scope = [
                        Function,
                        UserDefinedType,
                        VariableAssignation,
                        ControlStructure,
                        UserDefinedEnum,
                        GlobalScope]

    def run(self, context):
        """
            Catches LBRACE tokens
            Creates new scope based on previous instruction or set it to multiline if it
            is a control statement
        """
        i = context.skip_ws(0, nl=False)
        if context.check_token(i, "LBRACE") is False:
            return False, 0
        i += 1
        hist = context.history
        for item in hist[::-1]:
            if item == "IsEmptyLine" or item == "IsComment" or item == "IsPreprocessorStatement":
                continue
            if item not in ["IsControlStatement", "IsFuncDeclaration", "IsUserDefinedType"]:
                context.sub = context.scope.inner(ControlStructure)
                context.sub.multiline = True
                break
            else:
                context.scope.multiline = True
            break

        tmp = i
        #while context.peek_token(tmp) and (context.check_token(tmp, ["NEWLINE"])) is False:
        #    tmp += 1
        tmp = context.eol(tmp)
        if context.peek_token(tmp) is not None:
            i = tmp
        return True, i
