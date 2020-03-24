from rules import PrimaryRule
from context import GlobalScope, Function, ControlStructure, UserDefinedType


class IsAssignation(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.primary = True
        self.priority = 5
        self.scope = []

    def run(self, context):
        i = context.skip_ws(0)
        return False, 0
