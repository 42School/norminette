from rules import Rule
from scope import *

class CheckBlockStart(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsBlockStart"]

    def run(self, context):
        outer = context.scope.get_outer()
        if type(context.scope) == ControlStructure and outer is not None and type(outer) == ControlStructure:
            if outer.multiline == False:
                context.new_error("MULT_IN_SINGLE_INSTR", context.peek_token(0))
        return False, 0