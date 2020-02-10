from lexer import Token
from rules import Rule


class CheckVarDeclarations(Rule):
    def __init__(self):
        super().__init__()
        self.dependencies = []
        self.primary = True

    def check_vartype_prefix(self):
        pass

    def run(self, context):
        return False, 0
        pass
