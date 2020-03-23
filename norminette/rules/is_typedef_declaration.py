from rules import PrimaryRule, Rule
import context
from scope import GlobalScope

class IsTypedefDeclaration(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 1
        self.scope = []

    def run(self, context):
        i = 0
        if context.check_token(i, "TYPEDEF") is True:
            print ("Found typedef")
            return True, i + 1
        return False, 0